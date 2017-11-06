# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Xphorism.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # Вышеуказанный import может завершиться по другой причине. 
        # Чтобы избежать маскировки других исключения для Python 2 убедитесь,
        try:
            import django
        except ImportError:
            raise ImportError(
                u"Не могу импортировать Django. Вы уверены, что установиои и " + \
                u"сделали доступными пременную PYTHONPATH? Или, возможно, " + \
                u"забыли активировать виртуальное кружение?"
            )
        raise
    execute_from_command_line(sys.argv)
