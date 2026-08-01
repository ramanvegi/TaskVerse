import os
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Comment, Task


class Command(BaseCommand):
    help = 'Seed demo departments, employees, projects, and tasks for local testing.'

    def handle(self, *args, **options):
        today = timezone.localdate()

        users = self._seed_users()
        departments = self._seed_departments()
        employees = self._seed_employees(departments, users, today)
        projects = self._seed_projects(employees, today)
        tasks = self._seed_tasks(projects, employees, users, today)
        coverage = self._seed_department_coverage(today)
        comments = self._seed_comments(tasks + coverage['tasks'])

        self.stdout.write(
            self.style.SUCCESS(
                'Demo content ready: '
                f'{Department.objects.count()} departments, '
                f'{Employee.objects.count()} employees, '
                f'{Project.objects.count()} projects, '
                f'{Task.objects.count()} tasks, '
                f'{Comment.objects.count()} comments. '
                f'Added/updated {len(coverage["projects"])} department coverage projects, '
                f'{len(coverage["tasks"])} coverage tasks, and {len(comments)} seeded comment entries.'
            )
        )

    def _seed_users(self):
        User = get_user_model()
        user_rows = [
            {
                'key': 'raman',
                'username': 'raman',
                'email': 'raman@gmail.com',
                'first_name': 'Raman',
                'last_name': 'Vegi',
                'role': User.Role.EMPLOYEE,
                'phone_number': '9999991001',
                'password': os.getenv('TASKVERSE_RAMAN_PASSWORD', 'Dev#Pass725!2026'),
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'key': 'yaswanth',
                'username': 'yaswanth',
                'email': 'yaswanth@gmail.com',
                'first_name': 'Yaswanth',
                'last_name': 'Vegi',
                'role': User.Role.EMPLOYEE,
                'phone_number': '9999991002',
                'password': os.getenv('TASKVERSE_YASWANTH_PASSWORD', 'Yaswanth12345'),
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'key': 'admin',
                'username': 'taskverse_admin',
                'email': 'admin@smartems.local',
                'first_name': 'TaskVerse',
                'last_name': 'Admin',
                'role': User.Role.ADMIN,
                'phone_number': '9999990000',
                'password': os.getenv('TASKVERSE_ADMIN_PASSWORD', 'Admin#Pass725!2026'),
                'is_staff': True,
                'is_superuser': True,
            },
        ]

        users = {}
        for row in user_rows:
            password = row.pop('password')
            key = row.pop('key')
            email = row['email'].lower()
            user, _ = User.objects.update_or_create(
                email=email,
                defaults={
                    **row,
                    'email': email,
                    'is_active': True,
                    'is_email_verified': True,
                },
            )
            user.set_password(password)
            user.save(update_fields=['password'])
            users[key] = user
        return users

    def _seed_departments(self):
        department_rows = [
            {
                'code': 'ANGULAR',
                'name': 'Angular',
                'description': 'Angular frontend development team',
                'is_active': True,
            },
            {
                'code': 'PYTHON',
                'name': 'Python',
                'description': 'Python development team',
                'is_active': True,
            },
            {
                'code': 'JAVA',
                'name': 'Java',
                'description': 'Java backend development team',
                'is_active': True,
            },
            {
                'code': 'DM',
                'name': 'Digital Marketing',
                'description': 'Digital marketing team',
                'is_active': True,
            },
            {
                'code': 'SALES',
                'name': 'Sales',
                'description': 'Sales team',
                'is_active': True,
            },
            {
                'code': 'DA',
                'name': 'Data Analytics',
                'description': 'Data Analytics Team',
                'is_active': True,
            },
            {
                'code': 'ENG',
                'name': 'Engineering',
                'description': 'Builds product features, platform APIs, and automation.',
                'is_active': True,
            },
            {
                'code': 'OPS',
                'name': 'Operations',
                'description': 'Coordinates delivery operations and production support.',
                'is_active': True,
            },
            {
                'code': 'HR',
                'name': 'Human Resources',
                'description': 'Owns people programs, onboarding, and employee engagement.',
                'is_active': True,
            },
        ]

        departments = {}
        for row in department_rows:
            department, _ = Department.objects.update_or_create(
                code=row['code'],
                defaults={
                    'name': row['name'],
                    'description': row['description'],
                    'is_active': row['is_active'],
                },
            )
            departments[row['code']] = department
        return departments

    def _seed_employees(self, departments, users, today):
        employee_rows = [
            {
                'user': users['raman'],
                'department': departments['PYTHON'],
                'employee_code': 'EMP0001',
                'first_name': 'Raman',
                'last_name': 'Vegi',
                'email': 'raman@gmail.com',
                'phone_number': '+91-99999-91001',
                'job_title': 'Python Developer',
                'hire_date': today - timedelta(days=460),
                'status': Employee.Status.ACTIVE,
                'address': 'Hyderabad, Telangana',
            },
            {
                'user': users['yaswanth'],
                'department': departments['ANGULAR'],
                'employee_code': 'EMP0002',
                'first_name': 'Yaswanth',
                'last_name': 'Vegi',
                'email': 'yaswanth@gmail.com',
                'phone_number': '+91-99999-91002',
                'job_title': 'Angular Developer',
                'hire_date': today - timedelta(days=430),
                'status': Employee.Status.ACTIVE,
                'address': 'Hyderabad, Telangana',
            },
            {
                'user': users['admin'],
                'department': departments['ENG'],
                'employee_code': 'ADM-0001',
                'first_name': 'TaskVerse',
                'last_name': 'Admin',
                'email': 'admin@smartems.local',
                'phone_number': '+91-99999-90000',
                'job_title': 'System Administrator',
                'hire_date': today - timedelta(days=1000),
                'status': Employee.Status.ACTIVE,
                'address': 'Hyderabad, Telangana',
            },
            {
                'department': departments['ENG'],
                'employee_code': 'EMP-1001',
                'first_name': 'Aarav',
                'last_name': 'Reddy',
                'email': 'aarav.reddy@example.com',
                'phone_number': '+91-90000-1001',
                'job_title': 'Senior Backend Engineer',
                'hire_date': today - timedelta(days=720),
                'status': Employee.Status.ACTIVE,
                'address': 'Hyderabad, Telangana',
            },
            {
                'department': departments['ENG'],
                'employee_code': 'EMP-1002',
                'first_name': 'Meera',
                'last_name': 'Sharma',
                'email': 'meera.sharma@example.com',
                'phone_number': '+91-90000-1002',
                'job_title': 'Frontend Developer',
                'hire_date': today - timedelta(days=540),
                'status': Employee.Status.ACTIVE,
                'address': 'Bengaluru, Karnataka',
            },
            {
                'department': departments['OPS'],
                'employee_code': 'EMP-1003',
                'first_name': 'Vikram',
                'last_name': 'Patel',
                'email': 'vikram.patel@example.com',
                'phone_number': '+91-90000-1003',
                'job_title': 'Delivery Manager',
                'hire_date': today - timedelta(days=900),
                'status': Employee.Status.ACTIVE,
                'address': 'Pune, Maharashtra',
            },
            {
                'department': departments['HR'],
                'employee_code': 'EMP-1004',
                'first_name': 'Ananya',
                'last_name': 'Iyer',
                'email': 'ananya.iyer@example.com',
                'phone_number': '+91-90000-1004',
                'job_title': 'HR Business Partner',
                'hire_date': today - timedelta(days=365),
                'status': Employee.Status.ON_LEAVE,
                'address': 'Chennai, Tamil Nadu',
            },
            {
                'department': departments['OPS'],
                'employee_code': 'EMP-1005',
                'first_name': 'Rahul',
                'last_name': 'Nair',
                'email': 'rahul.nair@example.com',
                'phone_number': '+91-90000-1005',
                'job_title': 'QA Analyst',
                'hire_date': today - timedelta(days=280),
                'status': Employee.Status.INACTIVE,
                'address': 'Kochi, Kerala',
            },
        ]

        employees = {}
        for row in employee_rows:
            employee_code = row.pop('employee_code')
            user = row.get('user')
            if user:
                Employee.objects.filter(user=user).exclude(employee_code=employee_code).update(user=None)
            employee, _ = Employee.objects.update_or_create(employee_code=employee_code, defaults=row)
            employees[employee_code] = employee
        return employees

    def _seed_projects(self, employees, today):
        project_rows = [
            {
                'project_code': 'TV-WEB',
                'name': 'TaskVerse Web Portal',
                'description': 'Angular portal for employee, project, and task management.',
                'start_date': today - timedelta(days=45),
                'end_date': today + timedelta(days=75),
                'status': Project.Status.IN_PROGRESS,
                'is_active': True,
                'employee_codes': ['EMP0002', 'EMP-1001', 'EMP-1002', 'EMP-1003'],
            },
            {
                'project_code': 'TV-API',
                'name': 'TaskVerse API Stabilization',
                'description': 'Backend API hardening, filtering, reporting, and documentation.',
                'start_date': today - timedelta(days=20),
                'end_date': today + timedelta(days=45),
                'status': Project.Status.PLANNED,
                'is_active': True,
                'employee_codes': ['EMP0001', 'EMP-1001', 'EMP-1003', 'ADM-0001'],
            },
            {
                'project_code': 'TV-USER-CONTENT',
                'name': 'Restored User Demo Content',
                'description': 'Demo content project for Raman, Yaswanth, and admin account validation.',
                'start_date': today - timedelta(days=10),
                'end_date': today + timedelta(days=30),
                'status': Project.Status.IN_PROGRESS,
                'is_active': True,
                'employee_codes': ['EMP0001', 'EMP0002', 'ADM-0001'],
            },
            {
                'project_code': 'TV-HR',
                'name': 'Employee Onboarding Automation',
                'description': 'Workflow improvements for onboarding and department handoffs.',
                'start_date': today - timedelta(days=120),
                'end_date': today - timedelta(days=5),
                'status': Project.Status.COMPLETED,
                'is_active': False,
                'employee_codes': ['EMP-1002'],
            },
        ]

        projects = {}
        for row in project_rows:
            employee_codes = row.pop('employee_codes')
            project_code = row.pop('project_code')
            project, _ = Project.objects.update_or_create(project_code=project_code, defaults=row)
            project.employees.set([employees[code] for code in employee_codes])
            projects[project_code] = project
        return projects

    def _seed_tasks(self, projects, employees, users, today):
        task_rows = [
            {
                'project': projects['TV-USER-CONTENT'],
                'assigned_to': employees['EMP0001'],
                'created_by': users['admin'],
                'title': 'Raman backend API content check',
                'description': 'Restored Raman account task covering Python/API work and employee filtering.',
                'due_date': today + timedelta(days=4),
                'priority': Task.Priority.HIGH,
                'status': Task.Status.IN_PROGRESS,
            },
            {
                'project': projects['TV-USER-CONTENT'],
                'assigned_to': employees['EMP0002'],
                'created_by': users['admin'],
                'title': 'Yaswanth Angular UI content check',
                'description': 'Restored Yaswanth account task covering Angular UI work and comments.',
                'due_date': today + timedelta(days=6),
                'priority': Task.Priority.MEDIUM,
                'status': Task.Status.TODO,
            },
            {
                'project': projects['TV-USER-CONTENT'],
                'assigned_to': employees['ADM-0001'],
                'created_by': users['admin'],
                'title': 'Admin validate restored demo accounts',
                'description': 'Admin task for checking restored logins, sample users, and seeded content.',
                'due_date': today + timedelta(days=2),
                'priority': Task.Priority.HIGH,
                'status': Task.Status.IN_PROGRESS,
            },
            {
                'project': projects['TV-WEB'],
                'assigned_to': employees['EMP-1002'],
                'created_by': users['admin'],
                'title': 'Build employee filter panel',
                'description': 'Connect department and status filters to the employee list view.',
                'due_date': today + timedelta(days=7),
                'priority': Task.Priority.HIGH,
                'status': Task.Status.IN_PROGRESS,
            },
            {
                'project': projects['TV-WEB'],
                'assigned_to': employees['EMP-1001'],
                'created_by': users['admin'],
                'title': 'Review dashboard API metrics',
                'description': 'Validate dashboard counts and recent activity data.',
                'due_date': today + timedelta(days=12),
                'priority': Task.Priority.MEDIUM,
                'status': Task.Status.TODO,
            },
            {
                'project': projects['TV-API'],
                'assigned_to': employees['EMP0001'],
                'created_by': users['admin'],
                'title': 'Add backend search regression tests',
                'description': 'Cover search and filter parameters for departments, employees, projects, and tasks.',
                'due_date': today + timedelta(days=18),
                'priority': Task.Priority.HIGH,
                'status': Task.Status.TODO,
            },
            {
                'project': projects['TV-API'],
                'assigned_to': employees['EMP-1003'],
                'created_by': users['admin'],
                'title': 'Prepare release checklist',
                'description': 'Document deployment validation steps and rollback checklist.',
                'due_date': today + timedelta(days=21),
                'priority': Task.Priority.MEDIUM,
                'status': Task.Status.IN_PROGRESS,
            },
            {
                'project': projects['TV-HR'],
                'assigned_to': employees['EMP-1002'],
                'created_by': users['admin'],
                'title': 'Archive onboarding templates',
                'description': 'Move completed onboarding content into reusable templates.',
                'due_date': today - timedelta(days=10),
                'priority': Task.Priority.LOW,
                'status': Task.Status.COMPLETED,
            },
            {
                'project': projects['TV-API'],
                'assigned_to': employees['EMP-1003'],
                'created_by': users['admin'],
                'title': 'Resolve overdue API incident review',
                'description': 'A realistic overdue task: due date has passed and work is still in progress.',
                'due_date': today - timedelta(days=3),
                'priority': Task.Priority.HIGH,
                'status': Task.Status.IN_PROGRESS,
            },
            {
                'project': projects['TV-WEB'],
                'assigned_to': None,
                'created_by': users['admin'],
                'title': 'Unassigned accessibility review',
                'description': 'Example unassigned task for validating unassigned display and project filtering.',
                'due_date': today + timedelta(days=9),
                'priority': Task.Priority.LOW,
                'status': Task.Status.TODO,
            },
            {
                'project': projects['TV-WEB'],
                'assigned_to': employees['EMP-1002'],
                'created_by': users['admin'],
                'title': 'Complete task comments walkthrough',
                'description': 'Completed task with seeded comments for validating comment viewing.',
                'due_date': today - timedelta(days=1),
                'priority': Task.Priority.MEDIUM,
                'status': Task.Status.COMPLETED,
            },
        ]

        tasks = []
        for row in task_rows:
            task, _ = Task.objects.update_or_create(
                project=row['project'],
                title=row['title'],
                defaults={
                    'assigned_to': row['assigned_to'],
                    'description': row['description'],
                    'due_date': row['due_date'],
                    'priority': row['priority'],
                    'status': row['status'],
                },
            )
            tasks.append(task)
        return tasks

    def _seed_department_coverage(self, today):
        """Ensure every department has projects/tasks while keeping overdue examples realistic."""
        projects = []
        tasks = []
        overdue_department_codes = {'ENG', 'OPS', 'SALES'}

        for department in Department.objects.order_by('name'):
            employees = list(
                Employee.objects.filter(department=department, status=Employee.Status.ACTIVE).order_by('employee_code')
            )
            if not employees:
                employees = list(Employee.objects.filter(department=department).order_by('employee_code'))
            if not employees:
                employees = [self._ensure_department_employee(department, today)]

            token = self._code_token(department.code or department.name, department.id)
            project, _ = Project.objects.update_or_create(
                project_code=f'DEPT-{token}',
                defaults={
                    'name': f'{department.name} Department Delivery',
                    'description': f'Demo project covering work owned by the {department.name} department.',
                    'start_date': today - timedelta(days=30),
                    'end_date': today + timedelta(days=45),
                    'status': Project.Status.IN_PROGRESS if department.is_active else Project.Status.ON_HOLD,
                    'is_active': True,
                },
            )
            project.employees.set(employees)
            projects.append(project)

            owner = employees[0]
            reviewer = employees[1] if len(employees) > 1 else owner
            department_code = (department.code or '').upper()
            has_overdue_example = department_code in overdue_department_codes
            old_overdue_title = f'{department.name} overdue follow-up'
            follow_up_title = old_overdue_title if has_overdue_example else f'{department.name} priority follow-up'
            if not has_overdue_example:
                Task.objects.filter(project=project, title=old_overdue_title).delete()

            task_rows = [
                {
                    'title': f'{department.name} weekly execution plan',
                    'assigned_to': owner,
                    'description': f'Prepare and publish the weekly execution plan for {department.name}.',
                    'due_date': today + timedelta(days=5),
                    'priority': Task.Priority.MEDIUM,
                    'status': Task.Status.TODO,
                },
                {
                    'title': follow_up_title,
                    'assigned_to': reviewer,
                    'description': (
                        f'Overdue demo task for validating overdue visibility in {department.name}.'
                        if has_overdue_example
                        else f'High-priority follow-up for validating priority filtering in {department.name}.'
                    ),
                    'due_date': today - timedelta(days=4) if has_overdue_example else today + timedelta(days=8),
                    'priority': Task.Priority.HIGH,
                    'status': Task.Status.IN_PROGRESS,
                },
                {
                    'title': f'{department.name} documentation refresh',
                    'assigned_to': owner,
                    'description': f'Refresh internal documentation and handoff notes for {department.name}.',
                    'due_date': today + timedelta(days=14),
                    'priority': Task.Priority.LOW,
                    'status': Task.Status.IN_PROGRESS,
                },
            ]

            for row in task_rows:
                task, _ = Task.objects.update_or_create(
                    project=project,
                    title=row['title'],
                    defaults={
                        'assigned_to': row['assigned_to'],
                        'description': row['description'],
                        'due_date': row['due_date'],
                        'priority': row['priority'],
                        'status': row['status'],
                        'created_by': row.get('created_by'),
                    },
                )
                tasks.append(task)

        return {'projects': projects, 'tasks': tasks}

    def _seed_comments(self, tasks):
        comments = []
        for task in tasks:
            author = task.created_by
            messages = [
                f'Demo comment: please review progress for "{task.title}".',
                'Demo comment: latest update is visible in the task comments viewer.',
            ]
            for message in messages:
                comment, _ = Comment.objects.update_or_create(
                    task=task,
                    message=message,
                    defaults={'author': author},
                )
                comments.append(comment)
        return comments

    def _ensure_department_employee(self, department, today):
        token = self._code_token(department.code or department.name, department.id)
        employee, _ = Employee.objects.update_or_create(
            employee_code=f'DEMO-{token}',
            defaults={
                'department': department,
                'first_name': department.name.split()[0][:40] or 'Demo',
                'last_name': 'Member',
                'email': f'demo-{department.id}@taskverse.local',
                'phone_number': '+91-90000-0000',
                'job_title': f'{department.name} Coordinator',
                'hire_date': today - timedelta(days=180),
                'status': Employee.Status.ACTIVE,
                'address': 'Demo address',
            },
        )
        return employee

    def _code_token(self, value, fallback):
        token = ''.join(ch for ch in value.upper() if ch.isalnum())[:18]
        return token or f'DEPT{fallback}'

