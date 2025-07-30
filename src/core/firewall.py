import subprocess
from typing import List, Dict, Tuple
from datetime import datetime

class FirewallManager:
    def __init__(self):
        self.RULE_NAME = "Overwatch MiddleEast"
        self.IP_LIST = ["34.1.48.0/20", "34.152.84.0/23", "34.166.0.0/16", "34.177.48.0/23", "35.192.0.0/12", "34.32.0.0/11"]
    
    def run_command(self, command: str) -> Tuple[bool, str]:
        """Execute command and return success status and output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def get_existing_rules_by_ip(self) -> Dict[str, Dict[str, int]]:
        """Get detailed info about existing firewall rules that match our target IPs"""
        result = {
            "inbound": {"enabled": 0, "disabled": 0},
            "outbound": {"enabled": 0, "disabled": 0}
        }
        
        success, output = self.run_command('netsh advfirewall firewall show rule name=all')
        
        if success:
            analyzed_rules = self.analyze_rules(output)
            
            result["inbound"]["enabled"] = len(analyzed_rules["inbound"]["enabled"])
            result["inbound"]["disabled"] = len(analyzed_rules["inbound"]["disabled"])
            result["outbound"]["enabled"] = len(analyzed_rules["outbound"]["enabled"])
            result["outbound"]["disabled"] = len(analyzed_rules["outbound"]["disabled"])
        
        return result
    
    def analyze_rules(self, output: str) -> Dict[str, Dict[str, List[str]]]:
        """Analyze firewall rules and return detailed information"""
        result = {
            "inbound": {"enabled": [], "disabled": []},
            "outbound": {"enabled": [], "disabled": []}
        }
        
        rules = output.split("Rule Name:")
        
        for rule_text in rules[1:]:
            if not rule_text.strip():
                continue
            
            rule_name = rule_text.split('\n')[0].strip()
            
            is_target = False
            for ip in self.IP_LIST:
                if ip in rule_text or ip.split('/')[0] in rule_text:
                    is_target = True
                    break
            
            if is_target and "Block" in rule_text:
                direction = "outbound"
                for line in rule_text.split('\n'):
                    if "Direction:" in line:
                        if "In" in line:
                            direction = "inbound"
                        elif "Out" in line:
                            direction = "outbound"
                        break
                
                if "Enabled:" in rule_text:
                    for line in rule_text.split('\n'):
                        if "Enabled:" in line:
                            if "Yes" in line:
                                result[direction]["enabled"].append(rule_name)
                            elif "No" in line:
                                result[direction]["disabled"].append(rule_name)
                            break
        return result
    
    def rule_matches_target_ips(self, rule_text: str, target_ips: List[str]) -> bool:
        """Check if a rule matches our target IPs and is a blocking rule"""
        if "Action:" not in rule_text or "Block" not in rule_text:
            return False
            
        for ip in target_ips:
            base_ip = ip.split('/')[0]
            if ip in rule_text or base_ip in rule_text:
                return True
                
        if self.RULE_NAME in rule_text:
            return True
            
        if "34.1.48" in rule_text or "34.152.84" in rule_text or "34.166" in rule_text or "34.177.48" in rule_text:
            return True
            
        return False
    
    def create_firewall_rules(self) -> List[Tuple[str, bool, str]]:
        """Create new firewall rules and return results"""
        results = []
        ip_list_str = ",".join(self.IP_LIST)
        
        # Create inbound rule
        inbound_cmd = f'netsh advfirewall firewall add rule name="{self.RULE_NAME} - Inbound" dir=in action=block remoteip={ip_list_str} enable=yes'
        success, output = self.run_command(inbound_cmd)
        results.append(("inbound", success, output))
        
        # Create outbound rule
        outbound_cmd = f'netsh advfirewall firewall add rule name="{self.RULE_NAME} - Outbound" dir=out action=block remoteip={ip_list_str} enable=yes'
        success, output = self.run_command(outbound_cmd)
        results.append(("outbound", success, output))
        
        return results
    
    def enable_rules(self, rule_names: List[str]) -> List[Tuple[str, bool, str]]:
        """Enable firewall rules and return results"""
        results = []
        for rule_name in rule_names:
            cmd = f'netsh advfirewall firewall set rule name="{rule_name}" new enable=yes'
            success, output = self.run_command(cmd)
            results.append((rule_name, success, output))
        return results
    
    def disable_rules(self, rule_names: List[str]) -> List[Tuple[str, bool, str]]:
        """Disable firewall rules and return results"""
        results = []
        for rule_name in rule_names:
            cmd = f'netsh advfirewall firewall set rule name="{rule_name}" new enable=no'
            success, output = self.run_command(cmd)
            results.append((rule_name, success, output))
        return results
    
    def delete_rules(self, rule_names: List[str]) -> List[Tuple[str, bool, str]]:
        """Delete firewall rules and return results"""
        results = []
        for rule_name in rule_names:
            cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
            success, output = self.run_command(cmd)
            results.append((rule_name, success, output))
        return results