"""
Collection for uniform phantom with repeat images.
"""

from pumpia.module_handling.collections import ModuleGroup, BaseCollection
from pumpia.module_handling.fields.windows import FieldWindow
from pumpia.module_handling.fields.groups import FieldGroup
from pumpia.module_handling.fields.viewer_fields import MonochromeDicomViewerField
from pumpia.widgets.viewers import MonochromeDicomViewer
from pumpia.widgets.context_managers import AutoPhantomManager

from pumpia_uniform_phantom.modules.sub_snr import SubSNR
from pumpia_uniform_phantom.modules.uniformity import Uniformity


class RepeatImagesCollection(BaseCollection):
    """
    Collection for uniform phantom with repeated scans.
    """
    context_manager = AutoPhantomManager()
    title = "Uniform Phantom Repeat Collection"

    viewer1 = MonochromeDicomViewerField(row=0, column=0)
    viewer2 = MonochromeDicomViewerField(row=0, column=1)

    snr: SubSNR = SubSNR(verbose_name="SNR")

    uniformity1: Uniformity = Uniformity(verbose_name="Uniformity")
    uniformity2: Uniformity = Uniformity(verbose_name="Uniformity")

    snr_output: FieldWindow = FieldWindow(snr.fields.series_name1,
                                          snr.fields.series_name2,
                                          snr.fields.signal,
                                          snr.fields.noise,
                                          snr.fields.snr,
                                          snr.fields.cor_snr,
                                          verbose_name="SNR Output")
    image1_output: FieldWindow = FieldWindow(uniformity1.fields.series_name,
                                             uniformity1.fields.uniformity,
                                             verbose_name="Image 1 Results")
    image2_output: FieldWindow = FieldWindow(uniformity2.fields.series_name,
                                             uniformity2.fields.uniformity,
                                             verbose_name="Image 2 Results")
    full_results: FieldWindow = FieldWindow(snr.fields.series_name1,
                                            snr.fields.series_name2,
                                            snr.fields.signal,
                                            snr.fields.noise,
                                            snr.fields.snr,
                                            snr.fields.cor_snr,
                                            uniformity1.fields.uniformity,
                                            uniformity2.fields.uniformity,
                                            field_names=[None,
                                                         None,
                                                         None,
                                                         None,
                                                         None,
                                                         None,
                                                         "Image 1 Uniformity",
                                                         "Image 2 Uniformity"])

    series_name1: FieldGroup = FieldGroup(snr.fields.series_name1,
                                          uniformity1.fields.series_name)
    series_name2: FieldGroup = FieldGroup(snr.fields.series_name2,
                                          uniformity2.fields.series_name)
    size_group: FieldGroup = FieldGroup(uniformity1.fields.size,
                                        uniformity2.fields.size)
    kernel_group: FieldGroup = FieldGroup(uniformity1.fields.kernel_bool,
                                          uniformity2.fields.kernel_bool)

    uniformity_window: ModuleGroup = ModuleGroup(uniformity1,
                                                 uniformity2,
                                                 verbose_name="Uniformity")

    def on_image_load(self, viewer: MonochromeDicomViewer) -> None:
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
