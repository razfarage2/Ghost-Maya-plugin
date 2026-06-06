# src/pose_ghost/ui/pose_ghost_panel.py
from pose_ghost.core import OnionSettings, DisplayMode
from pose_ghost.ui.qt_compat import QtWidgets, QtCore, HAS_PYSIDE2, HAS_PYSIDE6
from pose_ghost.ui.ui_commands import UiCommandsProtocol

class PoseGhostPanel:
    """
    Compact Maya UI control surface for Pose Ghost.
    Separated from Maya/PySide widget creation if Qt is not available.
    """
    def __init__(self, commands: UiCommandsProtocol):
        self.commands = commands
        self.widget = None

    def build_ui(self):
        if not HAS_PYSIDE2 and not HAS_PYSIDE6:
            return None

        self.widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.widget)
        
        # --- Status ---
        status_layout = QtWidgets.QHBoxLayout()
        self.status_label = QtWidgets.QLabel("Status: Live")
        self.status_label.setStyleSheet("font-weight: bold;")
        self.heavy_rig_check = QtWidgets.QCheckBox("Heavy Rig Mode")
        self.heavy_rig_check.setToolTip("Disable auto-rebuild for heavy rigs")
        self.heavy_rig_check.toggled.connect(self._on_heavy_rig_mode_toggled)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.heavy_rig_check)
        layout.addLayout(status_layout)
        
        # --- Targets ---
        target_layout = QtWidgets.QHBoxLayout()
        self.target_root_field = QtWidgets.QLineEdit()
        self.target_root_field.setPlaceholderText("Target Root")
        btn_pick_target = QtWidgets.QPushButton("Pick")
        btn_pick_target.clicked.connect(self._on_pick_target)
        btn_scan_target = QtWidgets.QPushButton("Scan")
        btn_scan_target.clicked.connect(self._on_scan_target)
        target_layout.addWidget(self.target_root_field)
        target_layout.addWidget(btn_pick_target)
        target_layout.addWidget(btn_scan_target)
        layout.addLayout(target_layout)

        # --- Rig ---
        rig_layout = QtWidgets.QHBoxLayout()
        self.rig_root_field = QtWidgets.QLineEdit()
        self.rig_root_field.setPlaceholderText("Rig Root (Optional)")
        btn_pick_rig = QtWidgets.QPushButton("Pick")
        btn_pick_rig.clicked.connect(self._on_pick_rig)
        btn_scan_rig = QtWidgets.QPushButton("Scan")
        btn_scan_rig.clicked.connect(self._on_scan_rig)
        rig_layout.addWidget(self.rig_root_field)
        rig_layout.addWidget(btn_pick_rig)
        rig_layout.addWidget(btn_scan_rig)
        layout.addLayout(rig_layout)

        # --- Sampling ---
        sample_group = QtWidgets.QGroupBox("Sampling")
        s_layout = QtWidgets.QFormLayout(sample_group)
        
        self.sampling_mode_combo = QtWidgets.QComboBox()
        self.sampling_mode_combo.addItems(["Relative Frames", "Keyed Poses"])
        s_layout.addRow("Sampling Mode", self.sampling_mode_combo)

        self.prev_count_spin = QtWidgets.QSpinBox()
        self.prev_count_spin.setMinimum(0)
        self.prev_count_spin.setValue(3)
        self.prev_count_spin.valueChanged.connect(self._on_settings_changed)
        s_layout.addRow("Previous Count", self.prev_count_spin)

        self.next_count_spin = QtWidgets.QSpinBox()
        self.next_count_spin.setMinimum(0)
        self.next_count_spin.setValue(3)
        self.next_count_spin.valueChanged.connect(self._on_settings_changed)
        s_layout.addRow("Next Count", self.next_count_spin)

        self.frame_step_spin = QtWidgets.QDoubleSpinBox()
        self.frame_step_spin.setMinimum(0.1)
        self.frame_step_spin.setValue(1.0)
        self.frame_step_spin.valueChanged.connect(self._on_settings_changed)
        s_layout.addRow("Frame Step", self.frame_step_spin)

        self.clamp_check = QtWidgets.QCheckBox()
        self.clamp_check.setChecked(True)
        self.clamp_check.toggled.connect(self._on_settings_changed)
        s_layout.addRow("Clamp to Playback", self.clamp_check)

        layout.addWidget(sample_group)

        # --- Appearance ---
        app_group = QtWidgets.QGroupBox("Appearance")
        a_layout = QtWidgets.QFormLayout(app_group)

        self.display_mode_combo = QtWidgets.QComboBox()
        self.display_mode_combo.addItems(["Show Both", "Show Previous", "Show Next"])
        self.display_mode_combo.currentIndexChanged.connect(self._on_display_mode_changed)
        a_layout.addRow("Display Mode", self.display_mode_combo)

        # Colors (Placeholder logic for V1)
        self.prev_color_btn = QtWidgets.QPushButton("Blue")
        self.next_color_btn = QtWidgets.QPushButton("Red")
        a_layout.addRow("Previous Color", self.prev_color_btn)
        a_layout.addRow("Next Color", self.next_color_btn)

        self.opacity_spin = QtWidgets.QDoubleSpinBox()
        self.opacity_spin.setRange(0.0, 1.0)
        self.opacity_spin.setSingleStep(0.1)
        self.opacity_spin.setValue(0.5)
        self.opacity_spin.valueChanged.connect(self._on_appearance_changed)
        a_layout.addRow("Base Opacity", self.opacity_spin)

        self.falloff_check = QtWidgets.QCheckBox()
        self.falloff_check.setChecked(True)
        self.falloff_check.toggled.connect(self._on_appearance_changed)
        a_layout.addRow("Opacity Falloff", self.falloff_check)

        self.fade_strength_spin = QtWidgets.QDoubleSpinBox()
        self.fade_strength_spin.setRange(0.0, 1.0)
        self.fade_strength_spin.setSingleStep(0.1)
        self.fade_strength_spin.setValue(0.5)
        self.fade_strength_spin.valueChanged.connect(self._on_appearance_changed)
        a_layout.addRow("Fade Strength", self.fade_strength_spin)

        layout.addWidget(app_group)

        # --- Object List ---
        self.object_list = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("Target Objects (Check to Bypass)"))
        layout.addWidget(self.object_list)

        # --- Proxy Source ---
        proxy_layout = QtWidgets.QHBoxLayout()
        self.source_mode_combo = QtWidgets.QComboBox()
        self.source_mode_combo.addItems(["Original", "Proxy"])
        self.source_mode_combo.currentIndexChanged.connect(self._on_source_mode_changed)
        
        self.proxy_root_field = QtWidgets.QLineEdit()
        self.proxy_root_field.setPlaceholderText("Proxy Root")
        btn_pick_proxy = QtWidgets.QPushButton("Pick")
        btn_pick_proxy.clicked.connect(self._on_pick_proxy)
        
        proxy_layout.addWidget(self.source_mode_combo)
        proxy_layout.addWidget(self.proxy_root_field)
        proxy_layout.addWidget(btn_pick_proxy)
        layout.addLayout(proxy_layout)

        # --- Actions ---
        action_layout = QtWidgets.QHBoxLayout()
        self.btn_enable = QtWidgets.QPushButton("Disable") # Toggle state
        self.btn_enable.setCheckable(True)
        self.btn_enable.setChecked(True)
        self.btn_enable.toggled.connect(self._on_enable_toggled)
        
        btn_clear = QtWidgets.QPushButton("Clear Ghosts")
        btn_clear.clicked.connect(self.commands.clear_ghosts)
        
        btn_rebuild = QtWidgets.QPushButton("Force Rebuild")
        btn_rebuild.clicked.connect(self.commands.force_rebuild)
        
        btn_save = QtWidgets.QPushButton("Save Profile")
        btn_save.clicked.connect(self.commands.save_profile)

        action_layout.addWidget(self.btn_enable)
        action_layout.addWidget(btn_clear)
        action_layout.addWidget(btn_rebuild)
        action_layout.addWidget(btn_save)
        layout.addLayout(action_layout)

        return self.widget

    # --- Callbacks ---

    def _on_pick_target(self):
        path = self.commands.pick_target_root()
        if path:
            self.target_root_field.setText(path)

    def _on_scan_target(self):
        path = self.target_root_field.text()
        if path:
            self.commands.scan_target_root(path)

    def _on_pick_rig(self):
        path = self.commands.pick_rig_root()
        if path:
            self.rig_root_field.setText(path)

    def _on_scan_rig(self):
        path = self.rig_root_field.text()
        if path:
            self.commands.scan_rig_root(path)

    def _on_pick_proxy(self):
        # We assume commands.pick_target_root acts generically as a picker.
        # Or we can just use the same protocol method if we add one.
        # Let's just use a fake path for now.
        pass

    def _on_settings_changed(self):
        # Read and validate UI values
        prev = max(0, self.prev_count_spin.value())
        nxt = max(0, self.next_count_spin.value())
        step = max(0.1, self.frame_step_spin.value())
        clamp = self.clamp_check.isChecked()
        
        # We create a new OnionSettings with only sampling fields for now. 
        # Real integration would merge with current settings.
        settings = OnionSettings(
            previous_count=prev,
            next_count=nxt,
            frame_step=step,
            clamp_to_playback_range=clamp
        )
        self.commands.set_sampling_settings(settings)

    def _on_display_mode_changed(self, idx):
        modes = [DisplayMode.BOTH, DisplayMode.PREVIOUS, DisplayMode.NEXT]
        if 0 <= idx < len(modes):
            self.commands.set_display_mode(modes[idx])

    def _on_appearance_changed(self):
        opacity = min(1.0, max(0.0, self.opacity_spin.value()))
        fade = min(1.0, max(0.0, self.fade_strength_spin.value()))
        falloff = self.falloff_check.isChecked()
        
        settings = OnionSettings(
            base_opacity=opacity,
            opacity_falloff_enabled=falloff,
            fade_strength=fade
        )
        self.commands.set_appearance_settings(settings)

    def _on_source_mode_changed(self, idx):
        mode = "original" if idx == 0 else "proxy"
        proxy_root = self.proxy_root_field.text() if mode == "proxy" else None
        self.commands.set_ghost_source_mode(mode, proxy_root)

    def _on_enable_toggled(self, checked):
        if checked:
            self.btn_enable.setText("Disable")
            self.commands.enable()
        else:
            self.btn_enable.setText("Enable")
            self.commands.disable()

    def _on_heavy_rig_mode_toggled(self, checked):
        self.commands.set_heavy_rig_mode(checked)

    def set_status_text(self, text: str):
        if self.widget and getattr(self, 'status_label', None):
            self.status_label.setText(text)