from b3j0f.dmts.gitlab.store import GitLabStore
from b3j0f.dmts.gitlab.access.project import ProjectAccessor

store = GitLabStore(
    host='git.canopsis.net', ssl=True, login='jlabejof', pwd='Wylapeti'
)
from b3j0f.dmts.model.project import Project

name = 'testy'

test = store.getbyname(accessor='projects', name='testy')
if test is not None:
    test.delete()

test = store.create(name='testy', accessor='projects')
print test._id, test

test.save()
print 'ok'
print store.accessors['projects'].find()
