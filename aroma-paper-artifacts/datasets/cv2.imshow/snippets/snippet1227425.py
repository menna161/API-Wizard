from absl import app
from absl import flags
from absl import logging
import bme680
from colormap import TURBO_COLORMAP
import cv2
from edgetpu.detection.engine import DetectionEngine
import numpy as np
from PIL import Image
from purethermal import PureThermal
from smbus2 import SMBus
from time import time


def main(_):
    if FLAGS.detect:
        ambient = bme680.BME680(i2c_addr=bme680.I2C_ADDR_PRIMARY, i2c_device=SMBus(1))
        ambient.set_humidity_oversample(bme680.OS_2X)
        ambient.set_pressure_oversample(bme680.OS_4X)
        ambient.set_temperature_oversample(bme680.OS_8X)
        ambient.set_filter(bme680.FILTER_SIZE_3)
        ambient.set_gas_status(bme680.DISABLE_GAS_MEAS)
        face_detector = DetectionEngine(FLAGS.face_model)
    with PureThermal() as camera:
        input_shape = (camera.height(), camera.width())
        raw_buffer = np.zeros(input_shape, dtype=np.int16)
        scaled_buffer = np.zeros(input_shape, dtype=np.uint8)
        if FLAGS.detect:
            rgb_buffer = np.zeros((*input_shape, 3), dtype=np.uint8)
        if FLAGS.visualize:
            window_buffer = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        raw_scale_factor = ((FLAGS.max_temperature - FLAGS.min_temperature) // 255)
        window_scale_factor_x = (WINDOW_WIDTH / camera.width())
        window_scale_factor_y = (WINDOW_HEIGHT / camera.height())
        if FLAGS.visualize:
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while ((not FLAGS.visualize) or (cv2.getWindowProperty(WINDOW_NAME, 0) != (- 1))):
            try:
                start_time = time()
                if FLAGS.detect:
                    if (not ambient.get_sensor_data()):
                        logging.warning('Ambient sensor data not ready')
                    ambient_data = ambient.data
                    logging.debug(('Ambient temperature: %.f °C' % ambient_data.temperature))
                    logging.debug(('Ambient pressure: %.f hPa' % ambient_data.pressure))
                    logging.debug(('Ambient humidity: %.f %%' % ambient_data.humidity))
                with camera.frame_lock():
                    np.copyto(dst=raw_buffer, src=camera.frame())
                np.clip(((raw_buffer - FLAGS.min_temperature) // raw_scale_factor), 0, 255, out=scaled_buffer)
                cv2.normalize(src=scaled_buffer, dst=scaled_buffer, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
                if FLAGS.detect:
                    cv2.cvtColor(src=scaled_buffer, dst=rgb_buffer, code=cv2.COLOR_GRAY2RGB)
                    faces = face_detector.detect_with_image(Image.fromarray(rgb_buffer), threshold=FLAGS.face_confidence, top_k=FLAGS.max_num_faces, keep_aspect_ratio=True, relative_coord=False, resample=Image.BILINEAR)
                    if (len(faces) == 1):
                        logging.info('1 person')
                    else:
                        logging.info(('%d people' % len(faces)))
                    for face in faces:
                        temperature = get_temperature(raw_buffer, face.bounding_box)
                        if (not temperature):
                            logging.warning('Empty crop')
                            continue
                        logging.info(format_temperature(temperature))
                if FLAGS.visualize:
                    turbo_buffer = TURBO_COLORMAP[scaled_buffer]
                    cv2.cvtColor(src=turbo_buffer, dst=turbo_buffer, code=cv2.COLOR_RGB2BGR)
                    cv2.resize(src=turbo_buffer, dst=window_buffer, dsize=(WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC)
                    if FLAGS.detect:
                        for face in faces:
                            bbox = face.bounding_box
                            top_left = (int((window_scale_factor_x * bbox[(0, 0)])), int((window_scale_factor_y * bbox[(0, 1)])))
                            bottom_right = (int((window_scale_factor_x * bbox[(1, 0)])), int((window_scale_factor_y * bbox[(1, 1)])))
                            cv2.rectangle(window_buffer, top_left, bottom_right, LINE_COLOR, LINE_THICKNESS)
                            temperature = get_temperature(raw_buffer, face.bounding_box)
                            if (not temperature):
                                continue
                            label = format_temperature(temperature, add_unit=False)
                            (label_size, _) = cv2.getTextSize(label, LABEL_FONT, LABEL_SCALE, LABEL_THICKNESS)
                            label_position = ((((top_left[0] + bottom_right[0]) // 2) - (label_size[0] // 2)), (((top_left[1] + bottom_right[1]) // 2) + (label_size[1] // 2)))
                            cv2.putText(window_buffer, label, label_position, LABEL_FONT, LABEL_SCALE, LABEL_COLOR, LABEL_THICKNESS, cv2.LINE_AA)
                    cv2.imshow(WINDOW_NAME, window_buffer)
                    cv2.waitKey(1)
                duration = (time() - start_time)
                logging.debug(('Frame took %.f ms (%.2f Hz)' % ((duration * 1000), (1 / duration))))
            except KeyboardInterrupt:
                break
    if FLAGS.visualize:
        cv2.destroyAllWindows()
