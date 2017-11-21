from gitviper.gitconnector import connection

def get_ahead(branch):
	if not remote_exists(branch):
		return -1

	commits_ahead = connection.repo.iter_commits(str(branch.tracking_branch()) + ".." + branch.name)
	count_ahead = sum(1 for c in commits_ahead)

	return count_ahead

def get_behind(branch):
	if not remote_exists(branch):
		return -1

	commits_behind = connection.repo.iter_commits(branch.name + ".." + str(branch.tracking_branch()))
	count_behind = sum(1 for c in commits_behind)

	return count_behind

def remote_exists(branch):
	remotes = connection.repo.remotes

	if not remotes:
		return False

	for remote in remotes:
		branches =  list(remote.refs)

		for b in branches:
			if str(b.name) == str(branch.tracking_branch()):
				return True

	return False
