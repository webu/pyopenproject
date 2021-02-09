import json
import os

from business.exception.business_error import BusinessError
from model.form import Form
from model.user import User
from model.work_package import WorkPackage
from tests.test_cases.openproject_test_case import OpenProjectTestCase
from util.Filter import Filter


class WorkPackageServiceTestCase(OpenProjectTestCase):

    def setUp(self):
        super().setUp()
        WORK_PACKAGE = os.path.join(self.TEST_CASES, '../data/work_package.json')
        WORK_PACKAGE_FORM = os.path.join(self.TEST_CASES, '../data/work_package_form.json')
        RELATION = os.path.join(self.TEST_CASES, '../data/relation.json')
        USER = os.path.join(self.TEST_CASES, '../data/user.json')
        ACTIVITY = os.path.join(self.TEST_CASES, '../data/activity.json')
        ATTACHMENT = os.path.join(self.TEST_CASES, '../data/attachment.json')
        self.wpSer = self.factory.get_work_package_service()
        with open(WORK_PACKAGE) as f:
            self.work_package = WorkPackage(json.load(f))
        with open(WORK_PACKAGE_FORM) as f:
            self.work_package_form = Form(json.load(f))
        with open(RELATION) as f:
            self.relation = WorkPackage(json.load(f))
        with open(USER) as f:
            self.watcher = User(json.load(f))
        with open(ACTIVITY) as f:
            self.activity = WorkPackage(json.load(f))
        with open(ATTACHMENT) as f:
            self.attachment = WorkPackage(json.load(f))

    def new_work_package(self):
        wP = WorkPackage(self.wpSer.create_form()._embedded["payload"])
        wP.subject = "Demo task created by the API"
        project = self.wpSer.find_available_projects()[0].__dict__['_links']['self']
        wP._links["project"]["href"] = project['href']
        work_package_type = list(filter(
            lambda x: x.name == 'Task',
            self.factory.get_type_service().find_all()
        ))[0].__dict__['_links']['self']['href']
        wP.__dict__["_links"]["type"]["href"] = work_package_type
        return wP

    # TODO
    # def test_attachments(self):
    #     self.wpSer.add_attachment(self.work_package, self.attachment)
    #     self.assertIsNotNone(self.wpSer.find_attachments(self.work_package))

    def test_not_found(self):
        # There's no activity --> Exception
        with self.assertRaises(BusinessError):
            self.wpSer.find(self.work_package)

    def test_find(self):
        wP = self.new_work_package()
        wP = self.wpSer.create(wP)
        new_wP = self.wpSer.find(wP)
        # Work Package Found
        self.assertEqual(wP.subject, new_wP.subject)
        self.wpSer.delete(wP)

    def test_update(self):
        work_packages = self.wpSer.find_all()
        work_packages = list(filter(lambda x: x.lockVersion > 1, work_packages))
        work_package = WorkPackage({"id": work_packages[0].id, "lockVersion": work_packages[0].lockVersion})
        work_package.subject = "Changed subject"
        changed_wP = self.wpSer.update(work_package)
        self.assertEqual(work_package.id, changed_wP.id)
        self.assertEqual(work_package.subject, changed_wP.subject)
        work_package.subject = work_packages[0].subject
        work_package.lockVersion = changed_wP.lockVersion
        changed_wP = self.wpSer.update(work_package)
        self.assertEqual(work_package.id, changed_wP.id)
        self.assertEqual(work_package.subject, changed_wP.subject)

    def test_delete(self):
        wP = self.new_work_package()
        wP = self.wpSer.create(wP)
        self.wpSer.delete(wP)
        with self.assertRaises(BusinessError):
            self.wpSer.find(wP)

    # FIXME
    #  Error running request with the URL (HTTPError): 'http://127.0.0.1:8080/api/v3/work_packages/work_packages/schemas/4'.
    #  <!---- copyright
    #  OpenProject is a project management system.
    #  Copyright (C) 2012-2017 the OpenProject Foundation (OPF)
    #  This program is free software; you can redistribute it and/or
    #  modify it under the terms of the GNU General Public License version 3.
    #  OpenProject is a fork of ChiliProject, which is a fork of Redmine. The copyright follows:
    #  Copyright (C) 2006-2017 Jean-Philippe Lang
    #  Copyright (C) 2010-2013 the ChiliProject Team
    #  This program is free software; you can redistribute it and/or
    #  modify it under the terms of the GNU General Public License
    #  as published by the Free Software Foundation; either version 2
    #  of the License, or (at your option) any later version.
    #  This program is distributed in the hope that it will be useful,
    #  but WITHOUT ANY WARRANTY; without even the implied warranty of
    #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #  GNU General Public License for more details.
    #  You should have received a copy of the GNU General Public License
    #  along with this program; if not, write to the Free Software
    #  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
    #  See doc/COPYRIGHT.rdoc for more details.
    #  ++-->
    #  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    #     "http://www.w3.org/TR/html4/loose.dtd">
    #  <html>
    #  <title>OpenProject 404 error</title>
    #  <style>
    #  body{
    #  font-family: Trebuchet MS,Georgia,"Times New Roman",serif;
    #  color:#303030;
    #  margin:10px;
    #  }
    #  h1{
    #  font-size:1.5em;
    #  }
    #  p{
    #  font-size:0.8em;
    #  }
    #  </style>
    #  <body>
    #    <h1>Page not found</h1>
    #    <p>The page you were trying to access doesn't exist or has been removed.</p>
    #    <p><a href="javascript:history.back()">Back</a></p>
    #  </body>
    #  </html>
    def test_find_schema(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        schema = self.wpSer.find_schema(work_package)
        schemas = list(map(lambda x: x.__dict__, self.wpSer.find_all_schemas()))
        self.assertIn(schema.__dict__, schemas)

    def test_find_all_schemas(self):
        self.assertIsNotNone(self.wpSer.find_all_schemas([Filter("id", "=", ["12-1", "14-2"])]))

    def test_update_form(self):
        self.assertIsNotNone(self.wpSer.update_form(self.work_package))

    def test_find_all(self):
        work_packages = self.wpSer.find_all(25, 25, [Filter("type_id", "=", ["1", "2"])],
                                            '[["status", "asc"]]', "status", True)
        self.assertEqual(0, len(work_packages))

    def test_create(self):
        wP = self.new_work_package()
        # Without notify
        new_wP = self.wpSer.create(wP)
        new_wP = self.wpSer.find(new_wP)
        self.assertEqual(wP.subject, new_wP.subject)
        self.wpSer.delete(wP)

    def test_create_form(self):
        form = self.wpSer.create_form()
        self.assertEqual(self.work_package_form.__dict__["_embedded"]["payload"], form.__dict__["_embedded"]["payload"])

    def test_create_relation(self):
        work_packages = self.wpSer.find_all()
        work_packages = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))
        f = work_packages[0]
        t = work_packages[1]
        relation = self.wpSer.create_relation(
            type="follows",
            work_package_from=f,
            work_package_to=t,
            description="Demo relation created using the API")
        self.assertEqual("Demo relation created using the API", relation.description)
        self.assertEqual("follows", relation.type)
        self.assertEqual("precedes", relation.reverseType)
        self.factory.get_relation_service().delete(relation)

    def test_find_relations(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        relations = self.wpSer.find_relations(work_package)
        self.assertEqual(1, len(relations))

    # TODO: Not description enough to develop an easy gateway for this endpoint
    # def test_create_relation_form(self):
    #     form = self.wpSer.create_relation_form()

    def test_find_watchers(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        watchers = self.wpSer.find_watchers(work_package)
        self.assertEqual(0, len(watchers))

    def test_create_watcher(self):
        user = self.factory.get_user_service().find_all()[0]
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        watcher = self.wpSer.create_watcher(work_package, user)
        watchers = list(map(lambda x: x.__dict__, self.wpSer.find_watchers(work_package)))
        self.assertIn(watcher.__dict__, watchers)
        self.wpSer.delete_watcher(work_package, watcher)
        watchers = list(map(lambda x: x.__dict__, self.wpSer.find_watchers(work_package)))
        self.assertNotIn(watcher.__dict__, watchers)

    # FIXME
    #  {
    #  "_type":"Error",
    #  "errorIdentifier":"urn:openproject-org:api:v3:errors:InvalidQuery",
    #  "message":"Status filter has invalid values."
    #  }
    def test_find_relation_candidates(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        relations = self.wpSer.find_relation_candidates(work_package, query="rollout")
        self.assertEqual(0, len(relations))
        relations = self.wpSer.find_relation_candidates(work_package,
                                                        query="rollout",
                                                        # filters=[Filter("status_id", "o", ["null"])],
                                                        type="follows",
                                                        page_size=25)
        self.assertEqual(0, len(relations))

    def test_find_available_watchers(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        watchers = self.wpSer.find_available_watchers(work_package)
        self.assertEqual(2, len(watchers))

    def test_find_available_projects(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        projects = self.wpSer.find_available_projects(work_package)
        self.assertEqual(1, len(projects))

    def test_find_revisions(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        revisions = self.wpSer.find_revisions(work_package)
        self.assertEqual(0, len(revisions))

    def test_find_activities(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        activities = self.wpSer.find_activities(work_package)
        self.assertEqual(2, len(activities))

    def test_create_activity(self):
        work_packages = self.wpSer.find_all()
        work_package = list(filter(lambda x: x.__dict__["_links"]["status"]["title"] == "New", work_packages))[0]
        activity = self.wpSer.create_activity(work_package, "Comment added to the Work package")
        activities = list(map(lambda x: x.__dict__, self.wpSer.find_activities(work_package)))
        self.assertIn(activity.__dict__, activities)
