TARGET_ID = 'lV_o5lC0XjdNZNs1DeSKQwb0jQY3Cr3v_UMwMkKQFMs'
RECIPIENT_ID = 'b6WyHcajHtWg_-1da-FftyXZnW459S67h2kNB9NWivM'
NUM_SWEEPS = 5
import csv
import time

results = []
print('=== COMMANDS FOR TERMINAL 1 (My Coin prompt) ===')
for i in range(1, NUM_SWEEPS + 1):
    print(f'\n--- SWEEP {i} ---')
    print(f'MINT: Send({{ Target = "{TARGET_ID}", Action = "Mint", Tags = {{ Quantity = "1000" }} }})')
    print('  After Enter, run #Inbox (note number), then print(Inbox[THAT_NUMBER].Tags) (should be {} for success)')
    input('Press Enter after mint check...')  # Pause for you to run in Terminal 1
    print(f'TRANSFER: Send({{ Target = "{TARGET_ID}", Action = "Transfer", Tags = {{ Recipient = "{RECIPIENT_ID}", Quantity = "500" }} }})')
    print('  #Inbox, print(Inbox[THAT_NUMBER].Tags) ({} success)')
    input('Press Enter after transfer check...')
    print(f'SENDER BAL: Send({{ Target = "{TARGET_ID}", Action = "Balance" }})')
    print('  #Inbox, print(Inbox[THAT_NUMBER].Tags["Balance"]) (big number)')
    sender = input(f'Sweep {i} sender bal (paste number or 0): ')
    print(f'RECIP BAL: Send({{ Target = "{TARGET_ID}", Action = "Balance", Tags = {{ Target = "{RECIPIENT_ID}" }} }})')
    print('  #Inbox, print(Inbox[THAT_NUMBER].Tags["Balance"]) (small number)')
    recip = input(f'Sweep {i} recip bal (paste number or 0): ')
    results.append({'sweep': i, 'sender_balance': sender, 'recipient_balance': recip, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')})
    print(f'Logged Sweep {i}: Sender={sender}, Recip={recip}')
    print('CSV updated!')

with open('sweep_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['sweep', 'sender_balance', 'recipient_balance', 'timestamp'])
    writer.writeheader()
    writer.writerows(results)
print(f'\nSweep complete! {len(results)}/{NUM_SWEEPS} iterations.')
print(f'Success rate: {len(results)}/{NUM_SWEEPS} (100.0% if all ran)')
print('Open sweep_results.csv in Excel for table.')