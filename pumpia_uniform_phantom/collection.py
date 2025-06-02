"""
Collection for uniform phantom with repeat images.
"""

from pumpia.module_handling.module_collections import (OutputFrame,
                                                       WindowGroup,
                                                       BaseCollection)
from pumpia.module_handling.in_outs.viewer_ios import MonochromeDicomViewerIO
from pumpia.module_handling.in_outs.groups import IOGroup
from pumpia.widgets.viewers import BaseViewer
from pumpia.widgets.context_managers import AutoPhantomManagerGenerator

from pumpia_uniform_phantom.modules.sub_snr import SubSNR
from pumpia_uniform_phantom.modules.uniformity import Uniformity


class RepeatImagesCollection(BaseCollection):
    """
    Collection for uniform phantom with repeated scans.
    """
    context_manager_generator = AutoPhantomManagerGenerator()
    name = "Uniform Phantom Repeat Collection"

    viewer1 = MonochromeDicomViewerIO(row=0, column=0)
    viewer2 = MonochromeDicomViewerIO(row=0, column=1)

    snr = SubSNR(verbose_name="SNR")

    uniformity1 = Uniformity(verbose_name="Uniformity")
    uniformity2 = Uniformity(verbose_name="Uniformity")

    snr_output = OutputFrame(verbose_name="SNR Output")
    image1_output = OutputFrame(verbose_name="Image 1 Results")
    image2_output = OutputFrame(verbose_name="Image 2 Results")
    full_results = OutputFrame()

    uniformity_window = WindowGroup([uniformity1, uniformity2], verbose_name="Uniformity")

    def load_outputs(self):
        self.full_results.register_output(self.snr.signal)
        self.full_results.register_output(self.snr.noise)
        self.full_results.register_output(self.snr.snr)
        self.full_results.register_output(self.snr.cor_snr)
        self.full_results.register_output(self.uniformity1.uniformity,
                                          verbose_name="Image 1 Uniformity")
        self.full_results.register_output(self.uniformity2.uniformity,
                                          verbose_name="Image 2 Uniformity")

        self.snr_output.register_output(self.snr.signal)
        self.snr_output.register_output(self.snr.noise)
        self.snr_output.register_output(self.snr.snr)
        self.snr_output.register_output(self.snr.cor_snr)

        self.image1_output.register_output(self.uniformity1.uniformity)

        self.image2_output.register_output(self.uniformity2.uniformity)

        IOGroup([self.uniformity1.size, self.uniformity2.size])
        IOGroup([self.uniformity1.kernel_bool, self.uniformity2.kernel_bool])

    def on_image_load(self, viewer: BaseViewer) -> None:
        if viewer is self.viewer1:
            if self.viewer1.image is not None:
                image = self.viewer1.image
                self.snr.viewer1.load_image(image)
                self.uniformity1.viewer.load_image(image)
        elif viewer is self.viewer2:
            if self.viewer2.image is not None:
                image = self.viewer2.image
                self.snr.viewer2.load_image(image)
                self.uniformity2.viewer.load_image(image)
