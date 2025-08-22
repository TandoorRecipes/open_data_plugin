import os

# TODO if script fails on windows
# win + R →  gpedit.msc
# Computer Configuration → Windows Settings → Security Settings → Local Policies → User Rights Assignment → Create symbolic links
# add current user and restart PC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

VUE_BASE_PATH = os.path.join(BASE_DIR, 'vue3', 'src', 'plugins')
PLUGIN_VUE_BASE_PATH = os.path.join(BASE_DIR, 'recipes', 'plugins', 'open_data_plugin', 'frontend')

os.makedirs(VUE_BASE_PATH, exist_ok=True)

print(f'LINKING FROM {VUE_BASE_PATH} to {PLUGIN_VUE_BASE_PATH}')
links = [
    [PLUGIN_VUE_BASE_PATH, os.path.join(VUE_BASE_PATH, 'open_data_plugin')],
]

for l in links:
    try:
        os.symlink(l[0], l[1])
    except Exception:
        pass
