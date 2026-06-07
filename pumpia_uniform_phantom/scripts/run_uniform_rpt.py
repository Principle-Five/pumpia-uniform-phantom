# command line "python -m nuitka .\pumpia_uniform_phantom\scripts\run_uniform_rpt.py"

# tk-inter is needed for tkinter to work with nuitka
# nuitka documentation suggests it is not explicitly needed/found automatically but this is wrong
# (possibly due to inclusion of matplotlib)

# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --mode=onefile
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --user-package-configuration-file=dicoms.nuitka-package.config.yml

from pumpia_uniform_phantom.repeat.collection import RepeatImagesCollection


def run_repeat_uniform():
    RepeatImagesCollection.run()


if __name__ == "__main__":
    run_repeat_uniform()
