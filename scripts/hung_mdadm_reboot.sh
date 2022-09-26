# When md0 is stuck burning 100% CPU on one core after a "1st sunday of the month" mdadm mdcheck
# dmesg may show: task jbd2/md0 blocked for more than x seconds
# cat /proc/mdstat shows "Check" that doesn't move
echo s > /proc/sysrq-trigger  # Sync to disk; wait a few minutes
echo u > /proc/sysrq-trigger  # remount as read only
echo b > /proc/sysrq-trigger  # reboot without waiting for anything



# For the check cron,  Ubuntu 20.04 made it use a stupid systemd timer, so it's a hassle to deal with now
# To change the cron, use
# sudo systemctl edit --full mdcheck_start.timer
# OnCalendar changes the start time. Make sure to change the RandomizedDelaySec to something less assinine than 24h; try 5m maybe
# By default it runs in 6 hour chunks; change that with:
# sudo systemctl edit --full mdcheck_start.service
# and then there's also the continue scripts:
# sudo systemctl edit --full mdcheck_continue.timer
# sudo systemctl edit --full mdcheck_continue.service
