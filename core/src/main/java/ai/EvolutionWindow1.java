package ai;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.Line2D;
import java.util.*;
import java.util.List;

/**
 * 4像素神经网络：高速演化与定量定格仿真器 (高度具象化化学递质与多细胞多线索级联解说版)
 */
public class EvolutionWindow1 extends JFrame {
    private static final long serialVersionUID = 1L;

    private EvolutionPanel evolutionPanel;
    private JLabel statusLabel;
    private JSlider speedSlider; 
    private JButton startBtn;
    private JButton pauseBtn;
    private JButton resumeBtn;

    private JButton demoBtn;
    private JButton demoPauseBtn; 
    private JButton demoPrevBtn; 
    private JButton demoNextBtn; 
    
    private JCheckBox detailExplanationBox;
    private JTextArea logArea;

    private volatile long generationCount = 0;
    private volatile VisualOrganism volatileCurrentOrg = null;
    private volatile String volatileStageText = "等待开始...";
    
    private volatile boolean isRunning = false;
    private volatile boolean isPaused = false;
    private Thread evolutionThread = null;
    private javax.swing.Timer renderTimer = null;

    private List<DemoSnapshot> demoFrames = new ArrayList<>();
    private int currentDemoStep = -1; 
    private javax.swing.Timer demoTimer = null;

    // 1. 【改进】：将信号代号升级为生物学真实的具体递质类型
    public enum Chem { 多巴胺, 去甲肾上腺素, 谷氨酸, GABA, 无 }

    public EvolutionWindow1() {
        this.setTitle("4像素神经网络：高级仿真器 (具象化神经递质与多细胞独立详解)");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        GraphicsConfiguration gc = this.getGraphicsConfiguration();
        Rectangle bounds = gc.getBounds(); 
        Insets insets = Toolkit.getDefaultToolkit().getScreenInsets(gc); 
        
        int x = bounds.x + insets.left;
        int y = bounds.y + insets.top;
        int width = bounds.width - insets.left - insets.right; 
        int height = bounds.height - insets.top - insets.bottom; 
        
        this.setBounds(x, y, width, height);

        evolutionPanel = new EvolutionPanel();
        this.getContentPane().add(evolutionPanel, BorderLayout.CENTER);

        logArea = new JTextArea();
        logArea.setBackground(new Color(25, 25, 30));
        logArea.setForeground(new Color(230, 230, 230));
        logArea.setFont(new Font("微软雅黑", Font.PLAIN, 12));
        logArea.setEditable(false);
        logArea.setLineWrap(true);
        logArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(logArea);
        scrollPane.setPreferredSize(new Dimension(600, 0));
        scrollPane.setBorder(BorderFactory.createMatteBorder(0, 1, 0, 0, Color.DARK_GRAY));
        this.getContentPane().add(scrollPane, BorderLayout.EAST);

        JPanel southPanel = new JPanel();
        southPanel.setLayout(new BoxLayout(southPanel, BoxLayout.Y_AXIS));
        southPanel.setBackground(new Color(30, 35, 45));

        JPanel row1 = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 5));
        row1.setBackground(new Color(30, 35, 45));
        statusLabel = new JLabel("系统就绪，请点击开始。");
        statusLabel.setForeground(Color.YELLOW);
        statusLabel.setFont(new Font("微软雅黑", Font.BOLD, 13));
        startBtn = new JButton("开始新演化");
        pauseBtn = new JButton("暂停演化");
        resumeBtn = new JButton("继续演化");
        pauseBtn.setEnabled(false);
        resumeBtn.setEnabled(false);
        
        JLabel speedLabel = new JLabel("演化速度 (1-1000):");
        speedLabel.setForeground(Color.WHITE);
        speedSlider = new JSlider(JSlider.HORIZONTAL, 1, 1000, 500);
        speedSlider.setBackground(new Color(30, 35, 45));
        speedSlider.setPreferredSize(new Dimension(150, 20));

        row1.add(statusLabel);
        row1.add(startBtn);
        row1.add(pauseBtn);
        row1.add(resumeBtn);
        row1.add(speedLabel);
        row1.add(speedSlider);

        JPanel row2 = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 5));
        row2.setBackground(new Color(25, 30, 40));
        row2.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, Color.DARK_GRAY));
        
        demoBtn = new JButton("自动演示");
        demoPauseBtn = new JButton("演示暂停"); 
        demoPrevBtn = new JButton("后退"); 
        demoNextBtn = new JButton("前进"); 
        
        detailExplanationBox = new JCheckBox("显示生物学深度解说 (开启突触与条件反射涌现细节说明)");
        detailExplanationBox.setForeground(Color.CYAN);
        detailExplanationBox.setBackground(new Color(25, 30, 40));
        detailExplanationBox.setFont(new Font("微软雅黑", Font.BOLD, 12));
        detailExplanationBox.setSelected(true); 
        detailExplanationBox.addActionListener(e -> {
            if (!demoFrames.isEmpty() && currentDemoStep >= -1) {
                applyFrameToPanel(currentDemoStep);
            }
        });
        
        setDemoButtonsEnabled(false); 

        row2.add(demoBtn);
        row2.add(demoPauseBtn);
        row2.add(demoPrevBtn);
        row2.add(demoNextBtn);
        row2.add(detailExplanationBox); 

        southPanel.add(row1);
        southPanel.add(row2);
        this.getContentPane().add(southPanel, BorderLayout.SOUTH);

        startBtn.addActionListener(e -> startNewEvolution());
        pauseBtn.addActionListener(e -> {
            isPaused = true;
            pauseBtn.setEnabled(false);
            resumeBtn.setEnabled(true);
        });
        resumeBtn.addActionListener(e -> {
            isPaused = false;
            pauseBtn.setEnabled(true);
            resumeBtn.setEnabled(false);
        });

        demoBtn.addActionListener(e -> startDetailedDemo());
        demoPauseBtn.addActionListener(e -> toggleDemoPause()); 
        demoPrevBtn.addActionListener(e -> stepDemo(-1));
        demoNextBtn.addActionListener(e -> stepDemo(1));
    }

    private void setDemoButtonsEnabled(boolean enabled) {
        demoBtn.setEnabled(enabled);
        demoPauseBtn.setEnabled(enabled);
        demoPrevBtn.setEnabled(enabled);
        demoNextBtn.setEnabled(enabled);
    }

    private synchronized void startNewEvolution() {
        isRunning = false;
        isPaused = false;
        if (evolutionThread != null) evolutionThread.interrupt();
        if (renderTimer != null) renderTimer.stop();
        if (demoTimer != null) demoTimer.stop();

        demoFrames.clear();
        currentDemoStep = -1;
        demoPauseBtn.setText("演示暂停"); 

        generationCount = 0;
        volatileStageText = "加速冲刺中...";
        statusLabel.setText("演化中，请稍候...");
        statusLabel.setForeground(Color.YELLOW);
        logArea.setText("--- 新演化启动 ---\n正在盲目筛选闭环条件反射网络...\n");
        
        startBtn.setEnabled(false);
        pauseBtn.setEnabled(true);
        resumeBtn.setEnabled(false);
        setDemoButtonsEnabled(false); 

        renderTimer = new javax.swing.Timer(100, e -> {
            VisualOrganism snapshotOrg = volatileCurrentOrg;
            if (snapshotOrg != null) {
                evolutionPanel.updateOrganism(snapshotOrg, generationCount, volatileStageText);
            }
        });
        renderTimer.start();

        isRunning = true;
        evolutionThread = new Thread(() -> {
            while (isRunning) {
                if (isPaused) {
                    try { Thread.sleep(50); } catch (InterruptedException ex) { return; }
                    continue;
                }

                generationCount++;
                int speed = speedSlider.getValue();
                
                if (speed < 1000) {
                    try {
                        long sleepTime = (1000 - speed) / 20;
                        if (sleepTime > 0) Thread.sleep(sleepTime);
                    } catch (InterruptedException ex) { return; }
                }

                int dynamicNetWidth = evolutionPanel.getWidth();
                int dynamicNetHeight = evolutionPanel.getHeight() - evolutionPanel.GRAPHICS_Y_OFFSET - 40;
                if (dynamicNetWidth <= 0) dynamicNetWidth = 950; 
                if (dynamicNetHeight <= 0) dynamicNetHeight = 550;

                VisualOrganism org = VisualOrganism.createRandomOrganism(dynamicNetWidth, dynamicNetHeight);
                volatileCurrentOrg = org;

                org.forward(new boolean[]{true, true, false, false}, true, false);
                org.forward(new boolean[]{false, true, true, true}, false, true);

                boolean[] testEnemy = org.forward(new boolean[]{true, true, false, false}, false, false);
                if (!testEnemy[0] || testEnemy[1]) continue;

                boolean[] testFood = org.forward(new boolean[]{false, true, true, true}, false, false);
                if (!testFood[1] || testFood[0]) continue;

                boolean[] testNoise = org.forward(new boolean[]{false, false, false, true}, false, false);
                if (testNoise[0] || testNoise[1]) continue;

                renderTimer.stop();
                isRunning = false;

                org.optimizeSpatialLayout(dynamicNetWidth, dynamicNetHeight, evolutionPanel.NODE_RADIUS);

                org.forward(new boolean[]{true, true, false, false}, false, false);
                evolutionPanel.updateOrganism(org, generationCount, "进化成功！已涌现出闭环后天条件反射并优化连线布局。");

                SwingUtilities.invokeLater(() -> {
                    statusLabel.setText("🏆 演化成功！历经 " + generationCount + " 代。单步/演示已解锁！");
                    statusLabel.setForeground(new Color(46, 204, 113));
                    startBtn.setEnabled(true);
                    pauseBtn.setEnabled(false);
                    resumeBtn.setEnabled(false);
                    setDemoButtonsEnabled(true); 
                });
                break;
            }
        });
        evolutionThread.start();
    }

    private void initDemoSnapshotData() {
        if (volatileCurrentOrg == null) return;
        demoFrames.clear();

        VisualOrganism demoOrg = volatileCurrentOrg.cloneOrganism();
        generateDemoFramesForScenario(demoOrg, "【场景一：天敌近身盲测】", new boolean[]{true, true, false, false}, false, false);
        generateDemoFramesForScenario(demoOrg, "【场景二：食物出现盲测】", new boolean[]{false, true, true, true}, false, false);
        generateDemoFramesForScenario(demoOrg, "【场景三：纯杂音干扰盲测】", new boolean[]{false, false, false, true}, false, false);
    }

    private void startDetailedDemo() {
        if (volatileCurrentOrg == null) return;
        if (demoTimer != null) demoTimer.stop();

        initDemoSnapshotData();
        demoPauseBtn.setText("演示暂停"); 

        currentDemoStep = 0;
        applyFrameToPanel(currentDemoStep);

        setupDemoTimer();
        demoTimer.start();
    }

    private void setupDemoTimer() {
        demoTimer = new javax.swing.Timer(1500, e -> {
            if (currentDemoStep < demoFrames.size() - 1) {
                currentDemoStep++;
                applyFrameToPanel(currentDemoStep);
            } else {
                demoTimer.stop();
                logArea.append("\n\n===== 棋谱演示播放完毕 =====");
                logArea.setCaretPosition(logArea.getDocument().getLength());
            }
        });
    }

    // 2. 【核心重构】：动态扫描受到牵连的每一个细胞，生成独立的一对一精细拆解报告
    private void generateDemoFramesForScenario(VisualOrganism org, String scenarioName, boolean[] pixels, boolean pain, boolean sweet) {
        org.resetAllNodes();
        org.setInputs(pixels, pain, sweet);
        
        List<String> activeInputs = new ArrayList<>();
        if (pixels[0]) activeInputs.add("像素A");
        if (pixels[1]) activeInputs.add("像素B");
        if (pixels[2]) activeInputs.add("像素C");
        if (pixels[3]) activeInputs.add("像素D");
        if (pain) activeInputs.add("痛觉");
        if (sweet) activeInputs.add("甜味");
        String activeElementsStr = activeInputs.isEmpty() ? "无输入" : String.join(", ", activeInputs);

        // ==================== 步骤 1：外界刺激传入 ====================
        StringBuilder sbLog = new StringBuilder(scenarioName + "\n→ 环境信号射入受体层。\n");
        StringBuilder sbExp = new StringBuilder();
        for (String inName : activeInputs) {
            sbLog.append(String.format(" * [细胞 %s]：检测到高强度外部刺激输入（流值=100.0）。\n", inName));
            sbExp.append(String.format(" （%s详解）：感受器受到物理/化学刺激。细胞膜上的配体门控通道或光敏通道开启，正离子涌入，局部发生阶段性的电位去极化变动。\n", inName));
        }
        demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.0f, false));

        // ==================== 步骤 2：评估输入层放电 ====================
        org.evaluateLayer(0);
        sbLog = new StringBuilder("【神经元评估】输入层受体结算点放电状态：\n");
        sbExp = new StringBuilder();
        for (String name : VisualOrganism.INPUTS) {
            VisualNode n = org.allNodes.get(name);
            if (n.isActivated) {
                sbLog.append(String.format(" * [细胞 %s]：当前输入(%.1f) >= 阈值(%.1f) → 【放电触发】\n", n.id, n.currentInput, n.threshold));
                sbExp.append(String.format(" （%s放电机制）：动作电位（Action Potential）在轴丘彻底爆发，电压门控钠通道呈多米诺骨牌式全额开启，电信号开始向中枢轴突狂飙。\n", n.id));
            }
        }
        demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.0f, false));

        // ==================== 交互 3 轮循环 ====================
        for (int iter = 1; iter <= 3; iter++) {
            org.releaseChemicalsInLayer1();
            
            // A. 递质释放阶段
            sbLog = new StringBuilder(String.format("【第%d轮网络交互】中继层活性细胞释放神经递质：\n", iter));
            sbExp = new StringBuilder();
            boolean anyChem = false;
            for (VisualNode n : org.allNodes.values()) {
                if (n.layer == 1 && n.isActivated && n.releaseChem != Chem.无) {
                    anyChem = true;
                    sbLog.append(String.format(" * [细胞 %s]：胞体高频兴奋，向突触间隙喷洒大量【%s】。\n", n.id, n.releaseChem.name()));
                    sbExp.append(String.format(" （%s - %s分子机制）：突触小泡与前膜融合。%s作为特定的信号媒介，在突触间隙扩散，准备与后膜的离子型或代谢型受体锚定绑定。\n", n.id, n.releaseChem.name(), n.releaseChem.name()));
                }
            }
            if (!anyChem) {
                sbLog.append(" * [无中继细胞激活]：当前阶段未触发化学递质释放机制。\n");
                sbExp.append(" （详解）：由于无前级中继元件越过阈值，突触间隙保持静息，无囊泡胞吐发生。\n");
            }
            demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.3f + (iter * 0.23f), true));

            // B. 轴突连线电传导阶段
            org.propagateLinks();
            sbLog = new StringBuilder(String.format("【第%d轮网络交互】轴突电传导与突触时空总和：\n", iter));
            sbExp = new StringBuilder();
            
            // 找出本轮输入被改变的后级细胞
            Map<String, Double> incrementals = new HashMap<>();
            for (VisualLink link : org.links) {
                VisualNode from = org.allNodes.get(link.fromId);
                if (from.isActivated) {
                    incrementals.put(link.toId, incrementals.getOrDefault(link.toId, 0.0) + 100.0 * (link.weight / 100.0));
                }
            }
            for (Map.Entry<String, Double> entry : incrementals.entrySet()) {
                VisualNode toNode = org.allNodes.get(entry.getKey());
                sbLog.append(String.format(" * [细胞 %s]：通过前级轴突网络获得 +%.1f 的电位输入注入，当前累积输入值达到 %.1f。\n", toNode.id, entry.getValue(), toNode.currentInput));
                sbExp.append(String.format(" （%s时空总和）：该元件正在对突触后电位（EPSP/IPSP）进行时空总和。树突膜上的电容正在源源不断地积蓄跨膜电位。\n", toNode.id));
            }
            if (incrementals.isEmpty()) {
                sbLog.append(" * [无电信号流动]：本路径没有活性电信号流过轴突。\n");
                sbExp.append(" （详解）：前级无放电细胞，网络处于电位衰减周期。\n");
            }
            demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.3f + (iter * 0.23f), true));

            // C. 中继层细胞判定阶段
            org.evaluateLayer(1);
            sbLog = new StringBuilder(String.format("【第%d轮网络交互】中继层细胞结算判定：\n", iter));
            sbExp = new StringBuilder();
            for (VisualNode n : org.allNodes.values()) {
                if (n.layer == 1) {
                    if (n.isActivated) {
                        sbLog.append(String.format(" * [细胞 %s]：当前输入(%.1f) >= 阈值(%.1f) → 【产生爆发性去极化放电】\n", n.id, n.currentInput, n.threshold));
                        sbExp.append(String.format(" （%s放电详解）：输入总和越过临界点，激活了局部电压阀门，信号成功在中间核团实现逻辑接力与前传。\n", n.id));
                    }
                }
            }
            demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.3f + (iter * 0.23f), false));
        }

        // ==================== 步骤 4：效应器输出 ====================
        org.evaluateLayer(2);
        VisualNode flee = org.allNodes.get(VisualOrganism.ACTION_FLEE);
        VisualNode bite = org.allNodes.get(VisualOrganism.ACTION_BITE);
        
        sbLog = new StringBuilder("【执行效能输出】终层运动神经皮层判定：\n");
        sbExp = new StringBuilder();
        
        sbLog.append(String.format(" * [细胞 %s]：接收输入(%.1f), 阈值(%.1f) → %s\n", flee.id, flee.currentInput, flee.threshold, flee.isActivated ? "【触发逃逸肌肉阵挛！】" : "静息"));
        sbExp.append(flee.isActivated ? " （逃跑动作详解）：动作皮层放电引发了传出神经的运动神经冲动，骨骼肌纤维完成强直收缩，生命体在宏观上展现出逃避天敌的灵敏身手。\n" : " （逃跑静息）：该通路未获足够电位总和，动作被抑制。\n");
        
        sbLog.append(String.format(" * [细胞 %s]：接收输入(%.1f), 阈值(%.1f) → %s\n", bite.id, bite.currentInput, bite.threshold, bite.isActivated ? "【触发吞咽进食动作！】" : "静息"));
        sbExp.append(bite.isActivated ? " （进食动作详解）：引发咀嚼和吞咽神经回路激活，咬肌收缩，机体开始摄取外部营养。\n" : " （进食静息）：该动作被抑制，避免无意义的能量空耗。\n");
        
        demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.4f, false));

        // ==================== 步骤 5：突触可塑性修正 ====================
        sbLog = new StringBuilder("【突触修剪与赫布学习】突触结构权值漂移记录：\n");
        sbExp = new StringBuilder();
        boolean anyPlastic = false;
        
        // 预存可塑性漂移前的权重镜像以便对比
        for (VisualLink link : org.links) {
            if (link.modulatedBy != Chem.无 && org.activeChems.getOrDefault(link.modulatedBy, false)) {
                anyPlastic = true;
                double oldW = link.weight;
                double newW = Math.max(0, Math.min(100, link.weight + link.plasticityDelta));
                sbLog.append(String.format(" * [链接 %s → %s]：受到间隙高浓度【%s】调节，权重由 %.1f 变更为 %.1f（调整量: %.1f）。\n", 
                    link.fromId, link.toId, link.modulatedBy.name(), oldW, newW, link.plasticityDelta));
                sbExp.append(String.format(" （突触可塑性机制）：满足了Hebbian‘同频共振’或多巴胺调质强化规则。突触后膜突触后致密区（PSD）上的AMPA型受体数量发生物理增减，形成了真正的后天神经环路反射弧记忆。\n"));
            }
        }
        if (!anyPlastic) {
            sbLog.append(" * [无权重微调]：突触间隙没有环境调质气体或奖励分子喷洒，本轮未发生可塑性形态漂移。\n");
            sbExp.append(" （详解）：未达成‘痛苦强化’或‘生存奖励’条件，现有网络连接权值保持稳固状态。\n");
        }
        
        org.applyPlasticity();
        demoFrames.add(new DemoSnapshot(org, sbLog.toString(), sbExp.toString(), 0.0f, false));
    }

    private void applyFrameToPanel(int step) {
        if (step < -1 || step >= demoFrames.size()) return;

        if (step == -1) {
            VisualOrganism blankOrg = volatileCurrentOrg.cloneOrganism();
            blankOrg.resetAllNodes();
            evolutionPanel.updateOrganism(blankOrg, generationCount, "演示复盘中 - 初始就绪状态 [第0步]");
            
            String initText = "===== 📂 神经元逐体量化棋谱 =====\n\n[初始态] 系统处于完全干净的基础静息态。";
            if (detailExplanationBox.isSelected()) {
                initText += "\n\n（详解）：此时全网跨膜离子通道紧闭，维持经典内高钾、外高钠的静息电位(-70mV)。突触间隙没有多巴胺或谷氨酸等递质残留，处于信息捕获前的绝对零状态。请点击 [前进] 查看级联反应。";
            }
            logArea.setText(initText);
            return;
        }

        DemoSnapshot frame = demoFrames.get(step);
        evolutionPanel.updateOrganismSnapshot(frame, generationCount, "演示复盘中 - 步骤 [" + (step + 1) + "/" + demoFrames.size() + "]");
        
        StringBuilder sb = new StringBuilder("===== 📂 神经元逐体量化棋谱 =====\n\n");
        for (int i = 0; i <= step; i++) {
            sb.append("【步骤 ").append(i + 1).append("】\n")
              .append(demoFrames.get(i).logText);
            
            if (detailExplanationBox.isSelected()) {
                sb.append("\n🔬 --- 细胞显微学深度详解 ---\n")
                  .append(demoFrames.get(i).detailedBioExplanation);
            }
            sb.append("====================================================\n\n");
        }
        logArea.setText(sb.toString());
        logArea.setCaretPosition(logArea.getDocument().getLength());
    }

    private void toggleDemoPause() {
        if (demoTimer == null) return;
        if (demoTimer.isRunning()) {
            demoTimer.stop();
            demoPauseBtn.setText("继续演示");
        } else {
            if (currentDemoStep >= demoFrames.size() - 1) {
                startDetailedDemo();
            } else {
                demoPauseBtn.setText("演示暂停");
                demoTimer.start();
            }
        }
    }

    private void stepDemo(int direction) {
        if (demoTimer != null && demoTimer.isRunning()) {
            demoTimer.stop();
            demoPauseBtn.setText("继续演示");
        }
        if (demoFrames.isEmpty()) {
            initDemoSnapshotData();
            currentDemoStep = -1; 
        }
        int target = currentDemoStep + direction;
        if (target >= -1 && target < demoFrames.size()) {
            currentDemoStep = target;
            applyFrameToPanel(currentDemoStep);
        }
    }

    // =========================================================================
    // 内部类 1: 渲染面板
    // =========================================================================
    public class EvolutionPanel extends JPanel {
        private static final long serialVersionUID = 1L;

        private List<VisualLink> activeLinksSnapshot = null;
        private Map<String, VisualNode> activeNodesSnapshot = null;
        private Map<Chem, Float> chemIntensitySnapshot = null; 

        private long currentGeneration = 0;
        private String currentStageText = "等待进化开始...";
        
        public final int GRAPHICS_Y_OFFSET = 120;
        public final int NODE_RADIUS = 22;
        private VisualNode draggedNode = null;
        
        private final Map<Chem, List<Point>> segregatedParticleMaps = new HashMap<>();

        public EvolutionPanel() {
            this.setBackground(new Color(20, 24, 35));
            
            Chem[] chems = {Chem.多巴胺, Chem.去甲肾上腺素, Chem.谷氨酸, Chem.GABA};
            int[] seeds = {111, 444, 777, 999};
            double[] baseAngles = {0.0, Math.PI / 4, Math.PI / 2, Math.PI * 3 / 4};
            
            for (int cIdx = 0; cIdx < chems.length; cIdx++) {
                List<Point> offsets = new ArrayList<>();
                Random r = new Random(seeds[cIdx]);
                double angleOffset = baseAngles[cIdx];
                
                for (int i = 0; i < 24; i++) {
                    double angle = i * (Math.PI * 2 / 24) + angleOffset;
                    double dist = 28 + (cIdx * 6) + r.nextInt(15); 
                    int px = (int) (Math.cos(angle) * dist);
                    int py = (int) (Math.sin(angle) * dist);
                    offsets.add(new Point(px, py));
                }
                segregatedParticleMaps.put(chems[cIdx], offsets);
            }

            MouseAdapter mouseHandler = new MouseAdapter() {
                @Override
                public void mousePressed(MouseEvent e) {
                    if (activeNodesSnapshot == null) return;
                    int mouseX = e.getX();
                    int mouseY = e.getY() - GRAPHICS_Y_OFFSET;

                    for (VisualNode node : activeNodesSnapshot.values()) {
                        double distance = Math.sqrt(Math.pow(node.position.x - mouseX, 2) + Math.pow(node.position.y - mouseY, 2));
                        if (distance <= NODE_RADIUS) {
                            draggedNode = node;
                            break;
                        }
                    }
                }
                @Override
                public void mouseReleased(MouseEvent e) { draggedNode = null; }
                
                @Override
                public void mouseDragged(MouseEvent e) {
                    if (draggedNode != null) {
                        int newX = e.getX();
                        int newY = e.getY() - GRAPHICS_Y_OFFSET;
                        if (newX < 30) newX = 30;
                        if (newX > getWidth() - 30) newX = getWidth() - 30;
                        if (newY < 20) newY = 20;
                        if (newY > getHeight() - GRAPHICS_Y_OFFSET - 40) newY = getHeight() - GRAPHICS_Y_OFFSET - 40;

                        String nodeId = draggedNode.id;
                        draggedNode.position.setLocation(newX, newY);
                        
                        if (volatileCurrentOrg != null && volatileCurrentOrg.allNodes != null) {
                            VisualNode rootNode = volatileCurrentOrg.allNodes.get(nodeId);
                            if (rootNode != null) rootNode.position.setLocation(newX, newY);
                        }

                        for (DemoSnapshot frame : demoFrames) {
                            if (frame.snapshotNodes != null) {
                                VisualNode snapNode = frame.snapshotNodes.get(nodeId);
                                if (snapNode != null) snapNode.position.setLocation(newX, newY);
                            }
                        }
                        repaint();
                    }
                }
            };
            this.addMouseListener(mouseHandler);
            this.addMouseMotionListener(mouseHandler);
        }

        public void updateOrganism(VisualOrganism org, long generation, String stageText) {
            this.activeNodesSnapshot = org.allNodes;
            this.activeLinksSnapshot = org.links;
            this.currentGeneration = generation;
            this.currentStageText = stageText;
            
            this.chemIntensitySnapshot = new HashMap<>();
            for(Chem c : Chem.values()) {
                chemIntensitySnapshot.put(c, org.activeChems.get(c) ? 1.0f : 0.0f);
            }
            this.repaint();
        }

        public void updateOrganismSnapshot(DemoSnapshot snapshot, long generation, String stageText) {
            this.activeNodesSnapshot = snapshot.snapshotNodes;
            this.activeLinksSnapshot = snapshot.snapshotLinks;
            this.chemIntensitySnapshot = snapshot.snapshotChemIntensity;
            this.currentGeneration = generation;
            this.currentStageText = stageText;
            this.repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            if (activeNodesSnapshot == null) return;

            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            g2.setColor(Color.WHITE);
            g2.setFont(new Font("微软雅黑", Font.BOLD, 14));
            g2.drawString("演化筛选代数: " + currentGeneration, 30, 30);
            g2.setFont(new Font("微软雅黑", Font.PLAIN, 12));
            g2.setColor(new Color(200, 200, 200));
            g2.drawString("进程探针: " + currentStageText, 30, 55);

            // --- 动态生物色彩粒子群与具体递质标签名称绘制区 ---
            if (chemIntensitySnapshot != null) {
                for (VisualNode node : activeNodesSnapshot.values()) {
                    if (node.layer == 1 && node.releaseChem != Chem.无) {
                        float intensity = chemIntensitySnapshot.getOrDefault(node.releaseChem, 0.0f);
                        
                        if (intensity > 0.01f) {
                            Color particleColor;
                            switch(node.releaseChem) {
                                case 多巴胺: particleColor = new Color(241, 196, 15, (int)(intensity * 145)); break; // 金黄色
                                case 去甲肾上腺素: particleColor = new Color(155, 89, 182, (int)(intensity * 145)); break; // 幽灵紫
                                case 谷氨酸: particleColor = new Color(46, 204, 113, (int)(intensity * 145)); break; // 翡翠绿
                                case GABA: particleColor = new Color(230, 126, 34, (int)(intensity * 145)); break; // 活力橙
                                default: particleColor = new Color(255, 255, 255, 0);
                            }
                            
                            int cx = node.position.x;
                            int cy = node.position.y + GRAPHICS_Y_OFFSET;
                            
                            g2.setColor(particleColor);
                            List<Point> specificOffsets = segregatedParticleMaps.get(node.releaseChem);
                            if (specificOffsets != null) {
                                for (Point pt : specificOffsets) {
                                    g2.fillOval(cx + pt.x - 3, cy + pt.y - 3, 6, 6);
                                }
                            }
                            
                            // 1. 【改进】：在作图区随介质生成/小时，动态标出其生物化学类型名字标签
                            g2.setFont(new Font("微软雅黑", Font.BOLD, 11));
                            String chemLabel = "释放中: " + node.releaseChem.name();
                            int strWidth = g2.getFontMetrics().stringWidth(chemLabel);
                            
                            g2.setColor(new Color(15, 15, 20, (int)(intensity * 190)));
                            g2.fillRoundRect(cx + 25, cy - 35, strWidth + 10, 18, 5, 5);
                            g2.setColor(new Color(160, 160, 160, (int)(intensity * 150)));
                            g2.drawRoundRect(cx + 25, cy - 35, strWidth + 10, 18, 5, 5);
                            
                            Color textColor = new Color(particleColor.getRed(), particleColor.getGreen(), particleColor.getBlue(), 255);
                            g2.setColor(textColor);
                            g2.drawString(chemLabel, cx + 30, cy - 22);
                        }
                    }
                }
            }

            for (VisualLink link : activeLinksSnapshot) {
                VisualNode fromNode = activeNodesSnapshot.get(link.fromId);
                VisualNode toNode = activeNodesSnapshot.get(link.toId);
                if (fromNode == null || toNode == null) continue;

                float strokeWidth = 0.5f + (float) (link.weight / 100.0 * 4.5);
                g2.setStroke(new BasicStroke(strokeWidth));

                if (link.modulatedBy != Chem.无) {
                    g2.setColor(new Color(243, 156, 18, 140)); 
                } else {
                    g2.setColor(new Color(127, 140, 141, 70)); 
                }

                if (fromNode.isActivated && link.weight > 5) {
                    g2.setColor(Color.YELLOW); 
                }

                int x1 = fromNode.position.x;
                int y1 = fromNode.position.y + GRAPHICS_Y_OFFSET;
                int x2 = toNode.position.x;
                int y2 = toNode.position.y + GRAPHICS_Y_OFFSET;
                g2.drawLine(x1, y1, x2, y2);

                int midX = (x1 + x2) / 2;
                int midY = (y1 + y2) / 2;
                g2.setFont(new Font("Consolas", Font.BOLD, 10));
                if (fromNode.isActivated && link.weight > 5) {
                    g2.setColor(Color.GREEN);
                } else {
                    g2.setColor(new Color(52, 152, 219)); 
                }
                g2.drawString("W:" + (int)link.weight, midX - 10, midY - 2);
            }

            for (VisualNode node : activeNodesSnapshot.values()) {
                if (node.isActivated) {
                    if (node.id.equals("逃跑") || node.id.equals("痛觉")) {
                        g2.setColor(new Color(231, 76, 60));
                    } else if (node.id.equals("进食") || node.id.equals("甜味")) {
                        g2.setColor(new Color(46, 204, 113));
                    } else {
                        g2.setColor(new Color(52, 152, 219));
                    }
                } else {
                    g2.setColor(new Color(44, 62, 80));
                }

                int drawX = node.position.x;
                int drawY = node.position.y + GRAPHICS_Y_OFFSET;

                g2.fillOval(drawX - NODE_RADIUS, drawY - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2);
                g2.setStroke(new BasicStroke(1.5f));
                g2.setColor(Color.LIGHT_GRAY);
                g2.drawOval(drawX - NODE_RADIUS, drawY - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2);

                g2.setFont(new Font("Consolas", Font.PLAIN, 10));
                g2.setColor(Color.CYAN);
                g2.drawString("Th:" + (int)node.threshold, drawX - 16, drawY - 3);

                g2.setColor(Color.YELLOW);
                g2.drawString("In:" + (int)node.currentInput, drawX - 16, drawY + 8);

                g2.setFont(new Font("微软雅黑", Font.PLAIN, 11));
                g2.setColor(Color.WHITE);
                g2.drawString(node.id, drawX - NODE_RADIUS, drawY - NODE_RADIUS - 4);
                
                if (node.layer == 1 && node.releaseChem != Chem.无) {
                    g2.setFont(new Font("微软雅黑", Font.ITALIC, 10));
                    g2.setColor(Color.LIGHT_GRAY);
                    g2.drawString("配置:" + node.releaseChem.name(), drawX - NODE_RADIUS, drawY + NODE_RADIUS + 13);
                }
            }
        }
    }

    // =========================================================================
    // 内部类 2: 快照数据结构
    // =========================================================================
    public static class DemoSnapshot {
        public Map<String, VisualNode> snapshotNodes = new LinkedHashMap<>();
        public List<VisualLink> snapshotLinks = new ArrayList<>();
        public Map<Chem, Float> snapshotChemIntensity = new HashMap<>(); 
        public String logText;
        public String detailedBioExplanation; 

        public DemoSnapshot(VisualOrganism organism, String logText, String detailedBioExplanation, float fixedChemIntensity, boolean forceLayer1ChemShow) {
            this.logText = logText;
            this.detailedBioExplanation = detailedBioExplanation;
            
            for (Map.Entry<String, VisualNode> e : organism.allNodes.entrySet()) {
                VisualNode n = e.getValue();
                VisualNode copyNode = new VisualNode(n.id, n.threshold, n.releaseChem, n.layer, new Point(n.position));
                copyNode.isActivated = n.isActivated;
                copyNode.currentInput = n.currentInput;
                this.snapshotNodes.put(e.getKey(), copyNode);
            }
            for (VisualLink l : organism.links) {
                this.snapshotLinks.add(new VisualLink(l.fromId, l.toId, l.weight, l.modulatedBy, l.plasticityDelta));
            }
            
            for(Chem c : Chem.values()) {
                this.snapshotChemIntensity.put(c, 0.0f);
            }
            
            if (fixedChemIntensity > 0.001f) {
                for (VisualNode n : this.snapshotNodes.values()) {
                    if (n.layer == 1 && n.releaseChem != Chem.无) {
                        if (forceLayer1ChemShow || n.isActivated) {
                            this.snapshotChemIntensity.put(n.releaseChem, fixedChemIntensity);
                        }
                    }
                }
            }
        }
    }

    // =========================================================================
    // 内部类 3, 4, 5: 机体核心结构库
    // =========================================================================
    public static class VisualLink {
        public String fromId;
        public String toId;
        public double weight;
        public Chem modulatedBy = Chem.无;
        public double plasticityDelta = 0;

        public VisualLink(String fromId, String toId, double weight, Chem modulatedBy, double plasticityDelta) {
            this.fromId = fromId;
            this.toId = toId;
            this.weight = weight;
            this.modulatedBy = modulatedBy;
            this.plasticityDelta = plasticityDelta;
        }
    }

    public static class VisualNode {
        public String id;
        public double threshold;
        public double currentInput = 0;
        public boolean isActivated = false;
        public Chem releaseChem = Chem.无;
        public Point position; 
        public int layer;

        public VisualNode(String id, double threshold, Chem releaseChem, int layer, Point position) {
            this.id = id;
            this.threshold = threshold;
            this.releaseChem = releaseChem;
            this.layer = layer;
            this.position = position;
        }

        public void reset() { this.currentInput = 0; this.isActivated = false; }
        public void evaluate() { this.isActivated = (this.currentInput >= this.threshold); }
    }

    public static class VisualOrganism {
        public static final String[] INPUTS = {"像素A", "像素B", "像素C", "像素D", "痛觉", "甜味"};
        public static final String ACTION_FLEE = "逃跑";
        public static final String ACTION_BITE = "进食";

        public Map<String, VisualNode> allNodes = new LinkedHashMap<>();
        public List<VisualLink> links = new ArrayList<>();
        public Map<Chem, Boolean> activeChems = new HashMap<>();

        public static VisualOrganism createRandomOrganism(int netWidth, int netHeight) {
            VisualOrganism org = new VisualOrganism();
            Random rand = new Random();
            for (Chem c : Chem.values()) org.activeChems.put(c, false);

            int inputCount = INPUTS.length;
            for (int i = 0; i < inputCount; i++) {
                int y = 40 + i * (netHeight - 80) / (inputCount - 1);
                org.allNodes.put(INPUTS[i], new VisualNode(INPUTS[i], 10, Chem.无, 0, new Point(80, y)));
            }

            int index = 1;
            int colWidth = (netWidth - 160) / 3; 
            for (int col = 0; col < 2; col++) {
                for (int row = 0; row < 3; row++) {
                    String id = "中继" + index;
                    int x = 80 + (col + 1) * colWidth;
                    int y = 50 + row * (netHeight - 100) / 2;
                    org.allNodes.put(id, new VisualNode(id, 10 + rand.nextInt(140), Chem.values()[rand.nextInt(Chem.values().length - 1)], 1, 
                            new Point(x, y)));
                    index++;
                }
            }

            org.allNodes.put(ACTION_FLEE, new VisualNode(ACTION_FLEE, 50, Chem.无, 2, new Point(netWidth - 80, netHeight / 3)));
            org.allNodes.put(ACTION_BITE, new VisualNode(ACTION_BITE, 50, Chem.无, 2, new Point(netWidth - 80, (netHeight / 3) * 2)));

            List<String> allSrc = new ArrayList<>(org.allNodes.keySet());
            allSrc.remove(ACTION_FLEE); allSrc.remove(ACTION_BITE);
            List<String> allDst = new ArrayList<>(org.allNodes.keySet());
            for (String in : INPUTS) allDst.remove(in);

            int linkCount = 22 + rand.nextInt(12);
            for (int i = 0; i < linkCount; i++) {
                String src = allSrc.get(rand.nextInt(allSrc.size()));
                String dst = allDst.get(rand.nextInt(allDst.size()));
                if (src.equals(dst)) continue;
                org.links.add(new VisualLink(src, dst, rand.nextDouble() * 100, Chem.values()[rand.nextInt(Chem.values().length - 1)], rand.nextBoolean() ? 100 : -100));
            }
            return org;
        }

        public void optimizeSpatialLayout(int netWidth, int netHeight, int nodeRadius) {
            int colWidth = (netWidth - 160) / 3;
            int rowIdx = 0;
            for (VisualNode node : allNodes.values()) {
                if (node.layer == 1) {
                    int col = (rowIdx < 3) ? 0 : 1;
                    int row = rowIdx % 3;
                    int baseX = 80 + (col + 1) * colWidth;
                    int baseY = 65 + row * (netHeight - 130) / 2;
                    node.position.setLocation(baseX, baseY);
                    rowIdx++;
                }
            }

            int maxIterations = 30; 
            double safetyPadding = 6.0; 
            double dThreshold = nodeRadius + safetyPadding; 

            for (int iter = 0; iter < maxIterations; iter++) {
                boolean hasAdjustment = false;
                for (VisualNode mNode : allNodes.values()) {
                    if (mNode.layer != 1) continue; 
                    double forceX = 0; double forceY = 0;

                    for (VisualLink link : links) {
                        if (link.fromId.equals(mNode.id) || link.toId.equals(mNode.id)) continue;
                        VisualNode sNode = allNodes.get(link.fromId);
                        VisualNode dNode = allNodes.get(link.toId);
                        if (sNode == null || dNode == null) continue;

                        double dist = Line2D.ptSegDist(sNode.position.x, sNode.position.y, 
                                                       dNode.position.x, dNode.position.y, 
                                                       mNode.position.x, mNode.position.y);

                        if (dist < dThreshold) {
                            hasAdjustment = true;
                            if (dist < 0.001) { forceX += 15.0; forceY -= 10.0; continue; }

                            double dx = dNode.position.x - sNode.position.x;
                            double dy = dNode.position.y - sNode.position.y;
                            double len = Math.hypot(dx, dy);
                            if (len < 0.1) continue;

                            double t = ((mNode.position.x - sNode.position.x) * dx + (mNode.position.y - sNode.position.y) * dy) / (len * len);
                            t = Math.max(0, Math.min(1, t)); 
                            double closestX = sNode.position.x + t * dx;
                            double closestY = sNode.position.y + t * dy;

                            double pushX = mNode.position.x - closestX;
                            double pushY = mNode.position.y - closestY;
                            double pushDist = Math.hypot(pushX, pushY);
                            if (pushDist < 0.1) pushDist = 0.1;

                            double overlap = dThreshold - pushDist;
                            double factor = (overlap / dThreshold) * 12.0;

                            forceX += (pushX / pushDist) * factor;
                            forceY += (pushY / pushDist) * factor;
                        }
                    }

                    if (Math.hypot(forceX, forceY) > 0.01) {
                        int finalX = mNode.position.x + (int) Math.max(-25, Math.min(25, forceX));
                        int finalY = mNode.position.y + (int) Math.max(-25, Math.min(25, forceY));
                        finalX = Math.max(140, Math.min(netWidth - 140, finalX));
                        finalY = Math.max(40, Math.min(netHeight - 40, finalY));
                        mNode.position.setLocation(finalX, finalY);
                    }
                }
                if (!hasAdjustment) break;
            }
        }

        public void resetAllNodes() {
            for (VisualNode node : allNodes.values()) node.reset();
        }

        public void setInputs(boolean[] pixelInputs, boolean pain, boolean sweet) {
            allNodes.get("像素A").currentInput = pixelInputs[0] ? 100.0 : 0.0;
            allNodes.get("像素B").currentInput = pixelInputs[1] ? 100.0 : 0.0;
            allNodes.get("像素C").currentInput = pixelInputs[2] ? 100.0 : 0.0;
            allNodes.get("像素D").currentInput = pixelInputs[3] ? 100.0 : 0.0;
            allNodes.get("痛觉").currentInput = pain ? 100.0 : 0.0;
            allNodes.get("甜味").currentInput = sweet ? 100.0 : 0.0;
        }

        public void evaluateLayer(int layer) {
            for (VisualNode n : allNodes.values()) {
                if (n.layer == layer) n.evaluate();
            }
        }

        public void releaseChemicalsInLayer1() {
            for (VisualNode n : allNodes.values()) {
                if (n.layer == 1 && n.isActivated && n.releaseChem != Chem.无) {
                    activeChems.put(n.releaseChem, true);
                }
            }
        }

        public void propagateLinks() {
            for (VisualLink link : links) {
                VisualNode fromNode = allNodes.get(link.fromId);
                VisualNode toNode = allNodes.get(link.toId);
                double srcOut = fromNode.isActivated ? 100.0 : 0.0;
                toNode.currentInput += srcOut * (link.weight / 100.0);
            }
        }

        public void applyPlasticity() {
            for (VisualLink link : links) {
                if (link.modulatedBy != Chem.无 && activeChems.getOrDefault(link.modulatedBy, false)) {
                    link.weight = Math.max(0, Math.min(100, link.weight + link.plasticityDelta));
                }
            }
            for (Chem c : Chem.values()) activeChems.put(c, false);
        }

        public boolean[] forward(boolean[] pixelInputs, boolean pain, boolean sweet) {
            resetAllNodes();
            setInputs(pixelInputs, pain, sweet);
            evaluateLayer(0);
            for (int iter = 0; iter < 3; iter++) {
                evaluateLayer(1);
                releaseChemicalsInLayer1();
                propagateLinks();
            }
            evaluateLayer(2);
            boolean fleeTriggered = allNodes.get(ACTION_FLEE).isActivated;
            boolean biteTriggered = allNodes.get(ACTION_BITE).isActivated;
            applyPlasticity();
            return new boolean[]{fleeTriggered, biteTriggered};
        }

        public VisualOrganism cloneOrganism() {
            VisualOrganism copy = new VisualOrganism();
            for (Chem c : Chem.values()) copy.activeChems.put(c, this.activeChems.get(c));
            for (Map.Entry<String, VisualNode> e : this.allNodes.entrySet()) {
                VisualNode n = e.getValue();
                VisualNode cn = new VisualNode(n.id, n.threshold, n.releaseChem, n.layer, new Point(n.position));
                cn.isActivated = n.isActivated;
                cn.currentInput = n.currentInput;
                copy.allNodes.put(e.getKey(), cn);
            }
            for (VisualLink l : this.links) {
                copy.links.add(new VisualLink(l.fromId, l.toId, l.weight, l.modulatedBy, l.plasticityDelta));
            }
            return copy;
        }
    }

    public static class main {
        public static void main(String[] args) {
            SwingUtilities.invokeLater(() -> {
                EvolutionWindow1 window = new EvolutionWindow1();
                window.setVisible(true);
            });
        }
    }
}