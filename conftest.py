# Pusty plik konfiguracyjny pytest.
# Jego obecność w katalogu głównym repo sprawia, że pytest dodaje ten katalog
# do sys.path — dzięki temu "import straznik" działa też przy zwykłym wywołaniu
# "pytest" (tak jak w pipeline CI), nie tylko przy "python -m pytest".
