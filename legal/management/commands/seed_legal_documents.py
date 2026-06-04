"""
Seed the LegalDocument table with the initial Terms and Privacy content
that was previously hard-coded in the frontend mock layer.

Usage:
    python manage.py seed_legal_documents
    python manage.py seed_legal_documents --overwrite   # force-update existing
"""

import datetime

from django.core.management.base import BaseCommand

from legal.models import LegalDocument

DOCUMENTS = [
    {
        'doc_type': 'terms',
        'language': 'en',
        'title': 'Terms of Service',
        'last_updated': datetime.date(2025, 4, 1),
        'sections': [
            {
                'id': 'general',
                'title': 'General Provisions',
                'content': (
                    "Welcome to Orrin, a premium music streaming platform operated by "
                    "Orrin Labs Inc. By accessing or using the Orrin application, website, "
                    "or any associated services, you agree to be bound by these Terms of Service. "
                    "We reserve the right to modify these Terms at any time. "
                    "The Service is intended solely for users who are 13 years of age or older."
                ),
            },
            {
                'id': 'account',
                'title': 'Account Registration & Responsibilities',
                'content': (
                    "To access certain features of the Service, you may be required to create an account. "
                    "You are solely responsible for maintaining the confidentiality of your account credentials "
                    "and for all activities that occur under your account. "
                    "Each account is personal and may not be shared or transferred. "
                    "We reserve the right to suspend or terminate your account if you violate these Terms."
                ),
            },
            {
                'id': 'content',
                'title': 'Content, Licenses & Intellectual Property',
                'content': (
                    "The Service and its content are the exclusive property of Orrin Labs Inc. and its licensors. "
                    "By submitting content to the Service, you grant Orrin Labs Inc. a worldwide, non-exclusive, "
                    "royalty-free license to use that content in connection with the Service. "
                    "You agree not to submit content that infringes any intellectual property right."
                ),
            },
            {
                'id': 'termination',
                'title': 'Termination & Limitation of Liability',
                'content': (
                    "You may terminate your account at any time through the account settings page. "
                    "TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, ORRIN LABS INC. SHALL NOT BE "
                    "LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES. "
                    "THE SERVICE IS PROVIDED ON AN 'AS IS' AND 'AS AVAILABLE' BASIS WITHOUT WARRANTIES OF ANY KIND."
                ),
            },
        ],
    },
    {
        'doc_type': 'terms',
        'language': 'uk',
        'title': 'Умови використання',
        'last_updated': datetime.date(2025, 4, 1),
        'sections': [
            {
                'id': 'general',
                'title': 'Загальні положення',
                'content': (
                    "Ласкаво просимо до Orrin — преміального музичного стрімінгового сервісу, "
                    "що надається компанією Orrin Labs Inc. Використовуючи застосунок Orrin, "
                    "ви погоджуєтесь із цими Умовами використання. Ми залишаємо за собою право "
                    "змінювати ці Умови в будь-який час. Сервіс призначений для користувачів віком від 13 років."
                ),
            },
            {
                'id': 'account',
                'title': 'Реєстрація облікового запису та відповідальність',
                'content': (
                    "Для доступу до певних функцій Сервісу може знадобитися створення облікового запису. "
                    "Ви несете виключну відповідальність за збереження конфіденційності облікових даних "
                    "та за всі дії, що відбуваються в межах вашого облікового запису. "
                    "Ми залишаємо за собою право призупинити або припинити дію вашого облікового запису."
                ),
            },
            {
                'id': 'content',
                'title': 'Контент, ліцензії та інтелектуальна власність',
                'content': (
                    "Сервіс та його оригінальний контент є виключною власністю Orrin Labs Inc. та її ліцензіарів. "
                    "Надсилаючи контент до Сервісу, ви надаєте Orrin Labs Inc. всесвітню невиключну ліцензію "
                    "на використання цього контенту в рамках Сервісу."
                ),
            },
            {
                'id': 'termination',
                'title': 'Припинення дії та обмеження відповідальності',
                'content': (
                    "Ви можете видалити свій обліковий запис у будь-який час через налаштування. "
                    "У МАКСИМАЛЬНО ДОЗВОЛЕНОМУ ОБСЯЗІ ORRIN LABS INC. НЕ НЕСЕ ВІДПОВІДАЛЬНОСТІ "
                    "ЗА БУДЬ-ЯКІ НЕПРЯМІ АБО НАСЛІДКОВІ ЗБИТКИ. "
                    "СЕРВІС НАДАЄТЬСЯ НА УМОВАХ «ЯК Є» БЕЗ БУДЬ-ЯКИХ ГАРАНТІЙ."
                ),
            },
        ],
    },
    {
        'doc_type': 'privacy',
        'language': 'en',
        'title': 'Privacy Policy',
        'last_updated': datetime.date(2025, 4, 1),
        'sections': [
            {
                'id': 'general',
                'title': 'Information We Collect',
                'content': (
                    "Orrin Labs Inc. is committed to protecting your privacy. "
                    "We collect information you provide when creating an account, including your name, "
                    "email address, date of birth, and payment information. "
                    "We also automatically collect technical information such as your IP address, "
                    "device type, and interaction data."
                ),
            },
            {
                'id': 'account',
                'title': 'How We Use Your Information',
                'content': (
                    "We use the information we collect to provide, maintain, and improve the Service. "
                    "We use your listening history and preferences to generate personalised recommendations. "
                    "We may send promotional communications which you can opt out of at any time."
                ),
            },
            {
                'id': 'content',
                'title': 'Data Sharing & Third-Party Services',
                'content': (
                    "We do not sell your personal information to third parties. "
                    "We may share your information with service providers who perform services on our behalf. "
                    "We may use your information to display targeted advertising on the Service."
                ),
            },
            {
                'id': 'termination',
                'title': 'Your Rights & Data Retention',
                'content': (
                    "You may have the right to access, correct, delete, or port your personal information. "
                    "We retain your data for as long as your account is active. "
                    "When you delete your account, we will delete your personal information within 90 days. "
                    "Contact us at privacy@orrin.app with any questions."
                ),
            },
        ],
    },
    {
        'doc_type': 'privacy',
        'language': 'uk',
        'title': 'Політика конфіденційності',
        'last_updated': datetime.date(2025, 4, 1),
        'sections': [
            {
                'id': 'general',
                'title': 'Інформація, яку ми збираємо',
                'content': (
                    "Orrin Labs Inc. прагне захищати вашу конфіденційність. "
                    "Ми збираємо інформацію, яку ви надаєте під час створення облікового запису, "
                    "включаючи ваше ім'я, адресу електронної пошти та платіжні дані. "
                    "Ми також автоматично збираємо технічну інформацію про вашу взаємодію з Сервісом."
                ),
            },
            {
                'id': 'account',
                'title': 'Як ми використовуємо вашу інформацію',
                'content': (
                    "Ми використовуємо зібрану інформацію для надання, підтримки та вдосконалення Сервісу. "
                    "Ми використовуємо вашу історію прослуховування для формування персоналізованих рекомендацій. "
                    "Ви можете відмовитися від маркетингових повідомлень у будь-який час."
                ),
            },
            {
                'id': 'content',
                'title': 'Передача даних та сторонні сервіси',
                'content': (
                    "Ми не продаємо вашу персональну інформацію третім сторонам. "
                    "Ми можемо передавати вашу інформацію постачальникам послуг, "
                    "які виконують роботи від нашого імені."
                ),
            },
            {
                'id': 'termination',
                'title': 'Ваші права та зберігання даних',
                'content': (
                    "Залежно від вашої юрисдикції ви можете мати права на доступ, виправлення "
                    "або видалення вашої персональної інформації. "
                    "Ми зберігаємо вашу інформацію протягом усього терміну дії вашого облікового запису. "
                    "Зверніться до нас за адресою privacy@orrin.app з будь-якими запитаннями."
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the LegalDocument table with initial Terms and Privacy content.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Force-update existing records instead of skipping them.',
        )

    def handle(self, *args, **options):
        overwrite = options['overwrite']
        created_count = 0
        updated_count = 0
        skipped_count = 0

        for doc_data in DOCUMENTS:
            sections = doc_data.pop('sections')
            last_updated = doc_data.pop('last_updated')
            title = doc_data.pop('title')

            lookup = {k: doc_data[k] for k in ('doc_type', 'language')}
            existing = LegalDocument.objects.filter(**lookup).first()

            if existing:
                if overwrite:
                    existing.title = title
                    existing.last_updated = last_updated
                    existing.sections = sections
                    existing.save(update_fields=['title', 'last_updated', 'sections', 'updated_at'])
                    updated_count += 1
                    self.stdout.write(f'  Updated: {existing}')
                else:
                    skipped_count += 1
                    self.stdout.write(f'  Skipped (already exists): {existing}')
            else:
                LegalDocument.objects.create(
                    title=title,
                    last_updated=last_updated,
                    sections=sections,
                    **lookup,
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Created: {doc_data["doc_type"].upper()} [{doc_data["language"].upper()}]'
                    )
                )

            doc_data['sections'] = sections
            doc_data['last_updated'] = last_updated
            doc_data['title'] = title

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. Created: {created_count}, Updated: {updated_count}, '
                f'Skipped: {skipped_count}.'
            )
        )
