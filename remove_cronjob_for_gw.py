from fabric import Connection
from time import sleep
import subprocess
import pandas as pd
from subprocess import TimeoutExpired

hostlist = [
    "10.13.28.111"
]
username = 'pi'
password = 'iamgw_#@!'
# cron_job = '05 00 * * * sudo reboot'
output_file = 'gw_cronjob_results.xlsx'

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['IP Address', 'Cronjob removed'])

try:
    for hostname in hostlist:
        # Check if the gateway is pingable
        try:
            subprocess.run(['ping', '-c', '1', hostname], check=True, timeout=2)
        except TimeoutExpired:
            print(f"Gateway {hostname} is not reachable. Skipping.")
            # Add a row to the DataFrame with IP and Cronjob Added status as False
            result_df = pd.concat([result_df, pd.DataFrame({'IP Address': [hostname], 'Cronjob Added': [False]})], ignore_index=True)
            continue

        with Connection(
                host=hostname,
                user=username,
                connect_kwargs={"password": password},
                connect_timeout=2  # Set the timeout for the connection attempt
        ) as c:
            print(f"Removed cron job from {hostname}")

            # Create a cron job by appending the command to the crontab
            c.run(f"crontab -r", hide=True)

            print(f"Cron job removed successfully to {hostname}")

            # Add a row to the DataFrame with IP and Cronjob Added status as True
            result_df = pd.concat([result_df, pd.DataFrame({'IP Address': [hostname], 'Cronjob removed': [True]})], ignore_index=True)

        sleep(0.5)

except Exception as e:
    print(f"Error: {e}")

# Save the DataFrame to an Excel file
result_df.to_excel(f"download/{output_file}", index=False)
print(f"Results saved to {output_file}")
