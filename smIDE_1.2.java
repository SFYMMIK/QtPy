import javax.swing.*;
import javax.swing.text.DefaultEditorKit;
import javax.swing.text.JTextComponent;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;

public class SmIDE {

    private JFrame frame;
    private JTabbedPane tabbedPane;
    private JTextArea currentTextArea;
    private Map<String, JTextArea> textAreas;
    private String currentExtension;
    private String currentTab;

    public SmIDE() {
        initialize();
    }

    private void initialize() {
        frame = new JFrame("smIDE 1.2");
        frame.setSize(1250, 750);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        textAreas = new HashMap<>();

        createMenu();
        createNotebook();
        createToolbar();
        createNoteSpace();

        currentExtension = "";
        currentTab = null;

        frame.setVisible(true);
    }

    private void createMenu() {
        JMenuBar menuBar = new JMenuBar();

        JMenu fileMenu = new JMenu("File");
        fileMenu.setMnemonic('F');

        JMenuItem newMenuItem = new JMenuItem("New");
        newMenuItem.addActionListener(e -> newFile());
        fileMenu.add(newMenuItem);

        JMenuItem openMenuItem = new JMenuItem("Open");
        openMenuItem.addActionListener(e -> openFile());
        fileMenu.add(openMenuItem);

        JMenuItem saveMenuItem = new JMenuItem("Save");
        saveMenuItem.addActionListener(e -> saveFile());
        fileMenu.add(saveMenuItem);

        JMenuItem saveAsMenuItem = new JMenuItem("Save As");
        saveAsMenuItem.addActionListener(e -> saveFileAs());
        fileMenu.add(saveAsMenuItem);

        fileMenu.addSeparator();

        JMenuItem exitMenuItem = new JMenuItem("Exit");
        exitMenuItem.addActionListener(e -> frame.dispose());
        fileMenu.add(exitMenuItem);

        menuBar.add(fileMenu);

        frame.setJMenuBar(menuBar);
    }

    private void createNotebook() {
        tabbedPane = new JTabbedPane(JTabbedPane.TOP);

        String[] languages = {"HTML", "CSS", "SCSS", "JavaScript", "Python"};
        for (String lang : languages) {
            JTextArea textArea = createTextArea();
            JScrollPane scrollPane = new JScrollPane(textArea);
            tabbedPane.addTab(lang, scrollPane);
            textAreas.put(lang, textArea);
        }

        frame.add(tabbedPane);
        tabbedPane.addChangeListener(e -> onTabSelected());
    }

    private JTextArea createTextArea() {
        JTextArea textArea = new JTextArea();
        textArea.setLineWrap(true);
        textArea.setFont(new Font("helvetica", Font.PLAIN, 12));
        textArea.setBackground(new Color(40, 44, 52));
        textArea.setForeground(Color.WHITE);
        textArea.setCaretColor(Color.WHITE);
        return textArea;
    }

    private void createToolbar() {
        JToolBar toolbar = new JToolBar();

        JButton newButton = new JButton("New");
        newButton.addActionListener(e -> newFile());
        toolbar.add(newButton);

        JButton openButton = new JButton("Open");
        openButton.addActionListener(e -> openFile());
        toolbar.add(openButton);

        JButton saveButton = new JButton("Save");
        saveButton.addActionListener(e -> saveFile());
        toolbar.add(saveButton);

        JButton addButton = new JButton("+ add Tab +");
        addButton.addActionListener(e -> createNewTab());
        toolbar.add(addButton);

        frame.add(toolbar, BorderLayout.NORTH);
    }

    private void createNoteSpace() {
        JPanel noteSpacePanel = new JPanel();
        noteSpacePanel.setLayout(new BorderLayout());

        JLabel label = new JLabel("Notes");
        label.setFont(new Font("helvetica", Font.PLAIN, 12));
        label.setBorder(BorderFactory.createEmptyBorder(0, 0, 10, 0));
        noteSpacePanel.add(label, BorderLayout.NORTH);

        JTextArea noteTextArea = createTextArea();
        noteSpacePanel.add(new JScrollPane(noteTextArea), BorderLayout.CENTER);

        frame.add(noteSpacePanel, BorderLayout.WEST);
    }

    private void onTabSelected() {
        int index = tabbedPane.getSelectedIndex();
        currentTab = tabbedPane.getTitleAt(index);
        currentTextArea = textAreas.get(currentTab);

        Map<String, String> extensionMapping = Map.of(
                "HTML", "html",
                "CSS", "css",
                "SCSS", "scss",
                "JavaScript", "js",
                "Python", "py"
        );
        currentExtension = extensionMapping.get(currentTab);
    }

    private void openFile() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showOpenDialog(frame);

        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                String content = new String(Files.readAllBytes(selectedFile.toPath()));
                currentTextArea.setText(content);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void saveFile() {
        if (currentTab != null) {
            JFileChooser fileChooser = new JFileChooser();
            fileChooser.setSelectedFile(new File(currentTab + "." + currentExtension));
            int result = fileChooser.showSaveDialog(frame);

            if (result == JFileChooser.APPROVE_OPTION) {
                File selectedFile = fileChooser.getSelectedFile();
                try (FileWriter writer = new FileWriter(selectedFile)) {
                    writer.write(currentTextArea.getText());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } else {
            JOptionPane.showMessageDialog(frame, "Please select a tab to save.", "Save Error", JOptionPane.WARNING_MESSAGE);
        }
    }

    private void saveFileAs() {
        if (currentTab != null) {
            JFileChooser fileChooser = new JFileChooser();
            fileChooser.setSelectedFile(new File(currentTab + "." + currentExtension));
            int result = fileChooser.showSaveDialog(frame);

            if (result == JFileChooser.APPROVE_OPTION) {
                File selectedFile = fileChooser.getSelectedFile();
                try (FileWriter writer = new FileWriter(selectedFile)) {
                    writer.write(currentTextArea.getText());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } else {
            JOptionPane.showMessageDialog(frame, "Please select a tab to save.", "Save Error", JOptionPane.WARNING_MESSAGE);
        }
    }

    private void createNewTab() {
        String newTabName = JOptionPane.showInputDialog(frame, "Enter the name for the new tab:");
        if (newTabName != null && !newTabName.isEmpty()) {
            String[] languageOptions = {"Python", "HTML", "CSS", "SCSS", "JavaScript", "Undefined"};
            String selectedLanguage = (String) JOptionPane.showInputDialog(frame,
                    "Select a language for the new tab:",
                    "New Tab",
                    JOptionPane.QUESTION_MESSAGE,
                    null,
                    languageOptions,
                    "Undefined");

            if (selectedLanguage != null) {
                selectedLanguage = selectedLanguage.toLowerCase();
                if (!selectedLanguage.equalsIgnoreCase("Undefined") && !textAreas.containsKey(selectedLanguage)) {
                    createTab(newTabName, selectedLanguage);
                } else {
                    JOptionPane.showMessageDialog(frame, "Please select a valid language for the new tab.", "New Tab Error", JOptionPane.WARNING_MESSAGE);
                }
            }
        }
    }

    private void createTab(String tabName, String language) {
        JTextArea textArea = createTextArea();
        JScrollPane scrollPane = new JScrollPane(textArea);
        tabbedPane.addTab(tabName, scrollPane);
        textAreas.put(tabName, textArea);
        tabbedPane.setSelectedIndex(tabbedPane.indexOfTab(tabName));
        currentTextArea = textArea;
        currentTab = tabName;
        currentExtension = language;
    }

    private void newFile() {
        // Implement if needed
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(SmIDE::new);
    }
}
