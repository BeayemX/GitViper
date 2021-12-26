import gitviper.status as status
import gitviper.stash as stash
import gitviper.log as log
import gitviper.branches as branches
import gitviper.tasks as tasks

list_branches = branches.list_branches
list_logs = log.list_logs
list_status = status.list_status
list_stash = stash.list_stash

list_tasks = tasks.list_tasks
list_tasks_of_diff = tasks.list_tasks_of_diff