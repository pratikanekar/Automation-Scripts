from fabric import Connection
from time import sleep

hostlist = ['10.129.2.139']
username = 'pi'
password = 'iamgw_#@!'
cron_job = '05 00 * * * sudo reboot'

try:
    for hostname in hostlist:
        with Connection(
                host=hostname,
                user=username,
                connect_kwargs={"password": password}
        ) as c:
            print(f"Adding cron job to {hostname}: {cron_job}")

            # Create a cron job by appending the command to the crontab
            c.run(f"(crontab -l ; echo '{cron_job}') | sort | uniq | crontab -", hide=True)

            print(f"Cron job added successfully to {hostname}")
        sleep(0.5)

except Exception as e:
    print(f"Error: {e}")
