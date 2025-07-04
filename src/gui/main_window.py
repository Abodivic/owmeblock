import tkinter as tk
import customtkinter as ctk
import webbrowser
from typing import Dict

class MainWindow:
    def __init__(self, on_block_callback, on_unblock_callback, on_delete_callback, on_scan_callback):
        self.on_block_callback = on_block_callback
        self.on_unblock_callback = on_unblock_callback
        self.on_delete_callback = on_delete_callback
        self.on_scan_callback = on_scan_callback
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_gui()
    
    def setup_gui(self):
        """Initialize the GUI"""
        self.root = ctk.CTk()
        self.root.title("OW Middle East Blocker")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_main_content()
    
    def create_main_content(self):
        """Create main content area"""
        main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        
        self.create_status_section(main_frame)
        self.create_control_buttons(main_frame)
        self.create_log_section(main_frame)
    
    def create_status_section(self, parent):
        """Create status display section"""
        status_frame = ctk.CTkFrame(parent, height=40)
        status_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))
        status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="🔍 Scanning firewall rules...",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.status_label.pack(pady=12)
    
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = ctk.CTkFrame(parent, height=55)
        button_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=8)
        button_frame.grid_propagate(False)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.block_btn = ctk.CTkButton(
            button_frame,
            text="🚫 Block",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            command=self.on_block_callback,
            fg_color=("#D32F2F", "#F44336"),
            hover_color=("#B71C1C", "#D32F2F")
        )
        self.block_btn.grid(row=0, column=0, padx=8, pady=10, sticky="ew")
        
        self.unblock_btn = ctk.CTkButton(
            button_frame,
            text="✅ Unblock",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            command=self.on_unblock_callback,
            fg_color=("#4CAF50", "#66BB6A"),
            hover_color=("#388E3C", "#4CAF50")
        )
        self.unblock_btn.grid(row=0, column=1, padx=8, pady=10, sticky="ew")
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            command=self.on_delete_callback,
            fg_color=("#FF6F00", "#FF9800"),
            hover_color=("#E65100", "#FF6F00")
        )
        self.delete_btn.grid(row=0, column=2, padx=8, pady=10, sticky="ew")
    
    def create_log_section(self, parent):
        """Create log display section"""
        log_frame = ctk.CTkFrame(parent)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(8, 15))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="📋 Activity",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        log_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 5))
        
        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=9),
            wrap="word",
            height=240
        )
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 5))
        
        github_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        github_frame.grid(row=2, column=0, sticky="e", padx=12, pady=(3, 8))
        
        github_btn = ctk.CTkButton(
            github_frame,
            text="⚡ @Abodivic",
            font=ctk.CTkFont(size=9),
            height=20,
            width=70,
            command=self.open_github,
            fg_color="transparent",
            hover_color=("#F0F0F0", "#2B2B2B"),
            text_color=("#666666", "#AAAAAA"),
            border_width=1,
            border_color=("#CCCCCC", "#666666")
        )
        github_btn.pack(side="right")
    
    def update_status_display(self, rules: Dict[str, Dict[str, int]]):
        """Update the status display with rule information"""
        inbound_enabled = rules["inbound"]["enabled"]
        inbound_disabled = rules["inbound"]["disabled"]
        outbound_enabled = rules["outbound"]["enabled"]
        outbound_disabled = rules["outbound"]["disabled"]
        
        total_enabled = inbound_enabled + outbound_enabled
        total_disabled = inbound_disabled + outbound_disabled
        
        if total_enabled > 0:
            if total_disabled > 0:
                status_text = f"🟢 {total_enabled} rules active, {total_disabled} disabled"
                text_color = ("#4CAF50", "#66BB6A")
            else:
                status_text = f"🟢 {total_enabled} rules active - IPs blocked"
                text_color = ("#4CAF50", "#66BB6A")
        elif total_disabled > 0:
            status_text = f"🟡 {total_disabled} rules disabled - IPs not blocked"
            text_color = ("#FF9800", "#FFB74D")
        else:
            status_text = "🔴 No firewall rules found"
            text_color = ("#F44336", "#EF5350")
        
        self.status_label.configure(
            text=status_text,
            text_color=text_color
        )
        
        self.update_button_states(total_enabled, total_disabled)
    
    def update_button_states(self, enabled_count: int, disabled_count: int):
        """Update button states based on current rule status"""
        if enabled_count > 0:
            self.block_btn.configure(
                state="disabled",
                fg_color=("#404040", "#404040"),
                hover_color=("#404040", "#404040"),
                text_color=("#808080", "#808080")
            )
        else:
            self.block_btn.configure(
                state="normal",
                fg_color=("#D32F2F", "#F44336"),
                hover_color=("#B71C1C", "#D32F2F"),
                text_color=("#FFFFFF", "#FFFFFF")
            )
        
        if enabled_count == 0:
            self.unblock_btn.configure(
                state="disabled",
                fg_color=("#404040", "#404040"),
                hover_color=("#404040", "#404040"),
                text_color=("#808080", "#808080")
            )
        else:
            self.unblock_btn.configure(
                state="normal",
                fg_color=("#4CAF50", "#66BB6A"),
                hover_color=("#388E3C", "#4CAF50"),
                text_color=("#FFFFFF", "#FFFFFF")
            )
        
        if enabled_count == 0 and disabled_count == 0:
            self.delete_btn.configure(
                state="disabled",
                fg_color=("#404040", "#404040"),
                hover_color=("#404040", "#404040"),
                text_color=("#808080", "#808080")
            )
        else:
            self.delete_btn.configure(
                state="normal",
                fg_color=("#FF6F00", "#FF9800"),
                hover_color=("#E65100", "#FF6F00"),
                text_color=("#FFFFFF", "#FFFFFF")
            )
    
    def set_buttons_state(self, enabled: bool):
        """Enable or disable all buttons during operations"""
        if not enabled:
            for btn in [self.block_btn, self.unblock_btn, self.delete_btn]:
                btn.configure(
                    state="disabled",
                    fg_color=("#404040", "#404040"),
                    hover_color=("#404040", "#404040"),
                    text_color=("#808080", "#808080")
                )
    
    def open_github(self):
        """Open GitHub profile in default browser"""
        webbrowser.open("https://github.com/Abodivic/")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def get_log_widget(self):
        """Get the log text widget"""
        return self.log_text
    
    def get_root(self):
        """Get the root window"""
        return self.root