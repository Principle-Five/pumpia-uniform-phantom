"""
Integral uniformity module for uniform phantom
"""
import numpy as np
from scipy.signal import convolve2d

from pumpia.module_handling.modules import PhantomModule
from pumpia.module_handling.in_outs.roi_ios import InputGeneralROI
from pumpia.module_handling.in_outs.viewer_ios import MonochromeDicomViewerIO
from pumpia.module_handling.in_outs.simple import (PercInput,
                                                   BoolInput,
                                                   FloatOutput,
                                                   IntOutput)
from pumpia.image_handling.roi_structures import EllipseROI, RectangleROI
from pumpia.file_handling.dicom_structures import Series, Instance
from pumpia.module_handling.context import PhantomContext
from pumpia.widgets.context_managers import AutoPhantomManagerGenerator

LOW_PASS_KERNEL = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16


class Uniformity(PhantomModule):
    """
    Integral uniformity module for uniform phantom.
    """
    context_manager_generator = AutoPhantomManagerGenerator()
    viewer = MonochromeDicomViewerIO(row=0, column=0)

    size = PercInput(70, verbose_name="Size (%)")
    kernel_bool = BoolInput(verbose_name="Apply Low Pass Kernel")

    slice_used = IntOutput()
    uniformity = FloatOutput(verbose_name="Uniformity (%)")

    uniformity_roi = InputGeneralROI("Uniformity ROI", default_type="ROI rectangle")

    def draw_rois(self, context: PhantomContext, batch: bool = False) -> None:
        if isinstance(self.viewer.image, (Instance, Series)):
            factor = self.size.value / 100
            if context.shape == "rectangle":
                xmin = round(context.xcent - (factor * context.x_length / 2))
                xmax = round(context.xcent + (factor * context.x_length / 2))
                ymin = round(context.ycent - (factor * context.y_length / 2))
                ymax = round(context.ycent + (factor * context.y_length / 2))
                self.uniformity_roi.register_roi(RectangleROI(self.viewer.image,
                                                              xmin,
                                                              ymin,
                                                              xmax,
                                                              ymax,
                                                              slice_num=self.viewer.current_slice))
            else:
                a = round(factor * context.x_length / 2)
                b = round(factor * context.y_length / 2)
                self.uniformity_roi.register_roi(EllipseROI(self.viewer.image,
                                                            round(context.xcent),
                                                            round(context.ycent),
                                                            a,
                                                            b,
                                                            slice_num=self.viewer.current_slice))

    def post_roi_register(self, roi_input: InputGeneralROI):
        if (roi_input == self.uniformity_roi
            and self.uniformity_roi.roi is not None
                and self.manager is not None):
            self.manager.add_roi(self.uniformity_roi.roi)

    def link_rois_viewers(self):
        self.uniformity_roi.viewer = self.viewer

    def analyse(self, batch: bool = False):
        if self.uniformity_roi.roi is not None:
            roi = self.uniformity_roi.roi
            if self.kernel_bool.value:
                array = roi.image.array[0]
                array = convolve2d(array, LOW_PASS_KERNEL, mode="same")
                mask = roi.mask
                pixel_values = list(array[mask])
            else:
                pixel_values = roi.pixel_values

            max_val = max(pixel_values)
            min_val = min(pixel_values)
            uniformity = 100 * (1 - ((max_val - min_val) / (max_val + min_val)))  # type: ignore
            self.uniformity.value = uniformity
