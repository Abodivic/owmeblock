import threading
from typing import Dict

from ..core.firewall import FirewallManager
from ..utils.logger import Logger

class AppController:
    def __init__(self, gui, logger: Logger):
        self.gui = gui
        self.logger = logger
        self.firewall = FirewallManager()
        
        self.logger.set_log_widget(self.gui.get_log_widget(), self.gui.get_root())
    
    def scan_rules(self):
        """Scan for existing firewall rules"""
        self.logger.log_info("Scanning existing firewall rules...")
        self.gui.set_buttons_state(False)

        def scan_thread():
            try:
                rules = self.firewall.get_existing_rules_by_ip()
                self.gui.root.after(0, lambda: self.gui.update_status_display(rules))
                
                inbound_total = rules['inbound']['enabled'] + rules['inbound']['disabled']
                outbound_total = rules['outbound']['enabled'] + rules['outbound']['disabled']

                if inbound_total > 0 or outbound_total > 0:
                    inbound_msg = f"Inbound: {rules['inbound']['enabled']} active, {rules['inbound']['disabled']} disabled"
                    outbound_msg = f"Outbound: {rules['outbound']['enabled']} active, {rules['outbound']['disabled']} disabled"
                    self.gui.root.after(0, lambda: self.logger.log_success(f"Rule scan complete - {inbound_msg} | {outbound_msg}"))
                else:
                    self.gui.root.after(0, lambda: self.logger.log_info("No existing blocking rules found for target IPs"))

            except Exception as e:
                self.gui.root.after(0, lambda: self.logger.log_error(f"Error scanning rules: {str(e)}"))
                self.gui.root.after(0, lambda: self.gui.update_button_states(0, 0))

        threading.Thread(target=scan_thread, daemon=True).start()
    
    def block_ips(self):
        """Block the target IP addresses"""
        self.logger.log_info("Starting IP blocking process...")
        self.gui.set_buttons_state(False)
        
        def block_thread():
            try:
                success, output = self.firewall.run_command('netsh advfirewall firewall show rule name=all')
                if success:
                    analyzed_rules = self.firewall.analyze_rules(output)
                    enabled_count = 0
                    
                    all_disabled_rules = analyzed_rules["inbound"]["disabled"] + analyzed_rules["outbound"]["disabled"]
                    if all_disabled_rules:
                        results = self.firewall.enable_rules(all_disabled_rules)
                        for rule_name, success, output in results:
                            if success:
                                self.gui.root.after(0, lambda name=rule_name: self.logger.log_success(f"✅ Enabled existing rule: {name}"))
                                enabled_count += 1
                            else:
                                self.gui.root.after(0, lambda name=rule_name, out=output.strip(): self.logger.log_error(f"❌ Failed to enable rule {name}: {out}"))
                    
                    if analyzed_rules["inbound"]["enabled"] or analyzed_rules["outbound"]["enabled"]:
                        self.gui.root.after(0, lambda: self.logger.log_info("Some rules are already enabled"))
                    
                    if (not analyzed_rules["inbound"]["enabled"] and not analyzed_rules["inbound"]["disabled"] and
                        not analyzed_rules["outbound"]["enabled"] and not analyzed_rules["outbound"]["disabled"]):
                        
                        self.gui.root.after(0, lambda: self.logger.log_info("No existing rules found, creating new ones..."))
                        
                        results = self.firewall.create_firewall_rules()
                        for rule_type, success, output in results:
                            if success:
                                self.gui.root.after(0, lambda rt=rule_type: self.logger.log_success(f"✅ Created new {rt} rule"))
                            else:
                                self.gui.root.after(0, lambda rt=rule_type, out=output.strip(): self.logger.log_error(f"❌ Failed to create {rt} rule: {out}"))
                
                self.gui.root.after(0, lambda: self.logger.log_success("IP blocking completed! 🚫"))
                
            except Exception as e:
                self.gui.root.after(0, lambda: self.logger.log_error(f"Error during blocking: {str(e)}"))
            finally:
                self.gui.root.after(0, self.scan_rules)
        
        threading.Thread(target=block_thread, daemon=True).start()
    
    def unblock_ips(self):
        """Unblock the target IP addresses by disabling existing rules"""
        self.logger.log_info("Starting IP unblocking process...")
        self.gui.set_buttons_state(False)
        
        def unblock_thread():
            try:
                success, output = self.firewall.run_command('netsh advfirewall firewall show rule name=all')
                if not success:
                    self.gui.root.after(0, lambda: self.logger.log_error("Failed to get firewall rules for unblocking"))
                    return
                
                analyzed_rules = self.firewall.analyze_rules(output)
                disabled_count = 0
                
                all_enabled_rules = analyzed_rules["inbound"]["enabled"] + analyzed_rules["outbound"]["enabled"]
                if all_enabled_rules:
                    results = self.firewall.disable_rules(all_enabled_rules)
                    for rule_name, success, output in results:
                        if success:
                            self.gui.root.after(0, lambda name=rule_name: self.logger.log_success(f"✅ Disabled rule: {name}"))
                            disabled_count += 1
                        else:
                            self.gui.root.after(0, lambda name=rule_name, out=output.strip(): self.logger.log_error(f"❌ Failed to disable rule {name}: {out}"))
                
                if disabled_count == 0:
                    self.gui.root.after(0, lambda: self.logger.log_warning("No enabled target rules found to unblock"))
                else:
                    self.gui.root.after(0, lambda count=disabled_count: self.logger.log_success(f"Disabled {count} rules successfully"))
                
                self.gui.root.after(0, lambda: self.logger.log_success("IP unblocking completed! ✅"))
                
            except Exception as e:
                self.gui.root.after(0, lambda: self.logger.log_error(f"Error during unblocking: {str(e)}"))
            finally:
                self.gui.root.after(0, self.scan_rules)
        
        threading.Thread(target=unblock_thread, daemon=True).start()
    
    def delete_rules(self):
        """Delete all rules that contain our target IPs"""
        self.logger.log_info("Starting rule deletion process...")
        self.gui.set_buttons_state(False)
        
        def delete_thread():
            try:
                success, output = self.firewall.run_command('netsh advfirewall firewall show rule name=all')
                if not success:
                    self.gui.root.after(0, lambda: self.logger.log_error("Failed to get firewall rules for deletion"))
                    return
                
                analyzed_rules = self.firewall.analyze_rules(output)
                deleted_count = 0
                
                all_rules = (analyzed_rules["inbound"]["enabled"] + analyzed_rules["inbound"]["disabled"] +
                           analyzed_rules["outbound"]["enabled"] + analyzed_rules["outbound"]["disabled"])
                
                if all_rules:
                    results = self.firewall.delete_rules(all_rules)
                    for rule_name, success, output in results:
                        if success:
                            self.gui.root.after(0, lambda name=rule_name: self.logger.log_success(f"✅ Deleted rule: {name}"))
                            deleted_count += 1
                        else:
                            self.gui.root.after(0, lambda name=rule_name, out=output.strip(): self.logger.log_error(f"❌ Failed to delete rule {name}: {out}"))
                
                if deleted_count == 0:
                    self.gui.root.after(0, lambda: self.logger.log_warning("No target rules found to delete"))
                else:
                    self.gui.root.after(0, lambda count=deleted_count: self.logger.log_success(f"Deleted {count} rules successfully"))
                
                self.gui.root.after(0, lambda: self.logger.log_success("Rule deletion completed! 🗑️"))
                
            except Exception as e:
                self.gui.root.after(0, lambda: self.logger.log_error(f"Error during deletion: {str(e)}"))
            finally:
                self.gui.root.after(0, self.scan_rules)
        
        threading.Thread(target=delete_thread, daemon=True).start()