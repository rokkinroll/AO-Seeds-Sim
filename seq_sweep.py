from __future__ import annotations
import pexpect
from pexpect.popen_spawn import PopenSpawn
import json
import csv
import time
import re
from typing import Dict, List

# Config
NUM_SWEEPS = 5  # Number of sequence iterations
DELAY_SEC = 1  # Pause between actions
AOS_PATH = r"C:\Users\John\AppData\Roaming\npm\aos.cmd"  # Full path from 'where aos'

def connect_to_aos(process_name: str) -> PopenSpawn:
    """Spawn a connection to the named AOS process on Windows."""
    child = PopenSpawn([AOS_PATH, process_name], timeout=30)
    print(f"Started AOS for {process_name}. Waiting for startup...")
    time.sleep(3)  # Wait for startup
    # Print initial output
    initial_output = child.before.decode('utf-8')[-200:] if child.before else "No output yet"
    print("Initial output:", initial_output)
    
    # Menu fix: Up arrow to highlight 'aos' (cursor on 'hyper-aos' by default), then Enter
    child.send('\x1b[A')  # Up arrow
    time.sleep(1)
    arrow_output = child.before.decode('utf-8')[-200:] if child.before else "No output"
    print("Sent up arrow. Output after:", arrow_output)
    
    child.sendline('')  # Enter to select
    time.sleep(3)  # Wait for load
    enter_output = child.before.decode('utf-8')[-200:] if child.before else "No output"
    print("Sent Enter. Output after:", enter_output)
    
    # Try to match prompt (more lenient)
    try:
        child.expect(r'.*?\[Inbox:\d+\]>', timeout=20)
        print("Matched prompt! Final output:", child.after.decode('utf-8')[-200:])
    except pexpect.exceptions.TIMEOUT:
        print("Timeout on prompt match. Full output so far:", child.before.decode('utf-8') if child.before else "No output")
        raise
    return child

def get_process_id(child: PopenSpawn) -> str:
    """Get ao.id from the process."""
    child.sendline('ao.id')
    child.expect(r'.*?\[Inbox:\d+\]>', timeout=10)
    output = child.before.decode('utf-8')
    id_match = re.search(r'([a-zA-Z0-9_-]{43})', output)  # AO IDs are 43 chars
    if id_match:
        return id_match.group(1)
    raise ValueError("Failed to parse Process ID")

def execute_action(child: PopenSpawn, target: str, action: str, tags: Dict[str, str] = None) -> Dict:
    """Send a message via Send(), get last Inbox response, parse Data/Tags."""
    tags_str = json.dumps(tags or {})
    send_cmd = f'Send({{ Target = "{target}", Action = "{action}", Tags = {tags_str} }})'
    
    # Send the Send command
    child.sendline(send_cmd)
    child.expect(r'.*?\[Inbox:\d+\]>', timeout=15)
    
    # Get last inbox index
    child.sendline('#Inbox')
    child.expect(r'.*?\[Inbox:\d+\]>', timeout=10)
    index_match = re.search(r'(\d+)', child.before.decode('utf-8'))
    if not index_match:
        return {"success": False, "error": "Failed to get Inbox index"}
    index = index_match.group(1)
    
    # Get Data
    child.sendline(f'print(Inbox[{index}].Data or "nil")')
    child.expect(r'.*?\[Inbox:\d+\]>', timeout=10)
    before_str = child.before.decode('utf-8').strip()
    data_str = re.search(r'"([^"]*)"|(\d+)', before_str)
    data = data_str.group(1) or data_str.group(2) if data_str else None
    
    # Get Tags
    child.sendline(f'print(Inbox[{index}].Tags or {{}})')
    child.expect(r'.*?\[Inbox:\d+\]>', timeout=10)
    tags_str_raw = child.before.decode('utf-8').strip()
    tags = {}
    if tags_str_raw != "{}" and tags_str_raw != "nil":
        for match in re.findall(r'\["([^"]+)"\]=["\']([^"\']+)["\']', tags_str_raw):
            tags[match[0]] = match[1]
    
    child.sendline('')  # Clear
    
    return {
        "success": True,
        "data": data,
        "tags": tags
    }

def sweep_sequence() -> List[Dict]:
    """Run sweeps using connected AOS children."""
    token_child = connect_to_aos("token-sim")
    recipient_child = connect_to_aos("recipient-sim")
    
    try:
        TARGET_ID = get_process_id(token_child)
        RECIPIENT_ID = get_process_id(recipient_child)
        print(f"Auto-grabbed IDs: TARGET={TARGET_ID}, RECIPIENT={RECIPIENT_ID}")
        
        # Load token.lua in token process
        token_child.sendline('.load token.lua')
        token_child.expect(r'.*?\[Inbox:\d+\]>', timeout=10)
        
        results = []
        for i in range(1, NUM_SWEEPS + 1):
            print(f"\n--- Sweep {i}/{NUM_SWEEPS} ---")
            
            # Step 1: Mint
            mint_resp = execute_action(token_child, TARGET_ID, "Mint", {"Quantity": "1000"})
            if not mint_resp["success"]:
                print(f"Mint failed: {mint_resp.get('error')}")
                continue
            print(f"Minted 1000. Tags: {mint_resp['tags']}")
            time.sleep(DELAY_SEC)
            
            # Step 2: Transfer
            transfer_resp = execute_action(token_child, TARGET_ID, "Transfer", {"Recipient": RECIPIENT_ID, "Quantity": "500"})
            if not transfer_resp["success"]:
                print(f"Transfer failed: {transfer_resp.get('error')}")
                continue
            print(f"Transferred 500. Tags: {transfer_resp['tags']}")
            time.sleep(DELAY_SEC)
            
            # Step 3: Check balances
            sender_bal_resp = execute_action(token_child, TARGET_ID, "Balance")
            sender_bal = sender_bal_resp['tags'].get("Balance", "N/A")
            
            recip_bal_resp = execute_action(token_child, TARGET_ID, "Balance", {"Target": RECIPIENT_ID})
            recip_bal = recip_bal_resp['tags'].get("Balance", "N/A")
            
            result = {
                "sweep": i,
                "mint_success": mint_resp["success"],
                "transfer_success": transfer_resp["success"],
                "sender_balance": sender_bal,
                "recipient_balance": recip_bal,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)
            print(f"Balances: Sender={sender_bal}, Recipient={recip_bal}")
            time.sleep(DELAY_SEC)
        
        return results
    finally:
        token_child.sendline('.exit')
        recipient_child.sendline('.exit')
        token_child.close(force=True)
        recipient_child.close(force=True)

def save_results(results: List[Dict], filename: str = "sweep_results.csv"):
    """Save to CSV."""
    if not results:
        print("No results to save.")
        return
    fieldnames = results[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    try:
        sweep_results = sweep_sequence()
        save_results(sweep_results)
        print(f"\nSweep complete! {len(sweep_results)} iterations.")
        
        total_success = sum(1 for r in sweep_results if r["mint_success"] and r["transfer_success"])
        print(f"Success rate: {total_success}/{len(sweep_results)} ({100 * total_success / len(sweep_results):.1f}%)")
        
    except Exception as e:
        print(f"Script error: {e}")
        print("Tip: Check AOS version, or run manual tests in terminal.")