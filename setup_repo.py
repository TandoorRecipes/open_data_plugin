import os

# TODO if script fails on windows
# win + R →  gpedit.msc
# Computer Configuration → Windows Settings → Security Settings → Local Policies → User Rights Assignment → Create symbolic links
# add current user and restart PC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

VUE_BASE_PATH = os.path.join(BASE_DIR, 'vue')
PLUGIN_VUE_BASE_PATH = os.path.join(BASE_DIR, 'recipes', 'plugins', 'open_data_plugin', 'vue')

print(f'LINKING FROM {VUE_BASE_PATH} to {PLUGIN_VUE_BASE_PATH}')
# TODO IF ADDING LINKS make sure to add files to gitignore
links = [
    [os.path.join(VUE_BASE_PATH, 'package.json'), os.path.join(PLUGIN_VUE_BASE_PATH, 'package.json')],
    [os.path.join(VUE_BASE_PATH, 'yarn.lock'), os.path.join(PLUGIN_VUE_BASE_PATH, 'yarn.lock')],
    [os.path.join(VUE_BASE_PATH, '.yarnrc.yml'), os.path.join(PLUGIN_VUE_BASE_PATH, '.yarnrc.yml')],
    [os.path.join(VUE_BASE_PATH, 'tsconfig.json'), os.path.join(PLUGIN_VUE_BASE_PATH, 'tsconfig.json')],
    [os.path.join(VUE_BASE_PATH, 'babel.config.js'), os.path.join(PLUGIN_VUE_BASE_PATH, 'babel.config.js')],
    [os.path.join(VUE_BASE_PATH, 'babel.config.js.c'), os.path.join(PLUGIN_VUE_BASE_PATH, 'babel.config.js.c')],
    [os.path.join(VUE_BASE_PATH, 'node_modules'), os.path.join(PLUGIN_VUE_BASE_PATH, 'node_modules')],
    [os.path.join(VUE_BASE_PATH, 'src'), os.path.join(PLUGIN_VUE_BASE_PATH, 'src')],
]

for l in links:
    try:
        os.symlink(l[0], l[1])
    except Exception:
        print('failed to link')
        pass
