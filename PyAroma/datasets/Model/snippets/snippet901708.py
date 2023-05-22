from pynvml.nvml import *
import datetime
import collections
import time
from threading import Thread


@classmethod
def DeviceQuery(self, filter=None):
    '\n      Provides a Python interface to GPU management and monitoring functions.\n\n      This is a wrapper around the NVML library.\n      For information about the NVML library, see the NVML developer page\n      http://developer.nvidia.com/nvidia-management-library-nvml\n\n      Examples:\n      ---------------------------------------------------------------------------\n      For all elements as a list of dictionaries.  Similiar to nvisia-smi -q -x\n\n      $ DeviceQuery()\n\n      ---------------------------------------------------------------------------\n      For a list of filtered dictionary elements by string name.\n      Similiar ot nvidia-smi --query-gpu=pci.bus_id,memory.total,memory.free\n      See help_query_gpu.txt or DeviceQuery("--help_query_gpu") for available filter elements\n\n      $ DeviceQuery("pci.bus_id,memory.total,memory.free")\n\n      ---------------------------------------------------------------------------\n      For a list of filtered dictionary elements by enumeration value.\n      See help_query_gpu.txt or DeviceQuery("--help-query-gpu") for available filter elements\n\n      $ DeviceQuery([NVSMI_PCI_BUS_ID, NVSMI_MEMORY_TOTAL, NVSMI_MEMORY_FREE])\n\n      '
    if (filter is None):
        filter = [NVSMI_ALL]
    elif isinstance(filter, str):
        if ((filter == '--help') or (filter == '-h')):
            return nvidia_smi.DeviceQuery.__doc__
        elif (filter == '--help-query-gpu'):
            with open('help_query_gpu.txt', 'r') as fin:
                return fin.read()
        else:
            filter = nvidia_smi.__fromDeviceQueryString(filter)
    else:
        filter = list(filter)
    nvidia_smi_results = {}
    dictResult = []
    try:
        if ((NVSMI_ALL in filter) or (NVSMI_TIMESTAMP in filter)):
            nvidia_smi_results['timestamp'] = nvidia_smi.__toString(datetime.date.today())
        if ((NVSMI_ALL in filter) or (NVSMI_DRIVER_VERSION in filter)):
            nvidia_smi_results['driver_version'] = nvidia_smi.__toString(nvmlSystemGetDriverVersion())
        deviceCount = nvmlDeviceGetCount()
        if ((NVSMI_ALL in filter) or (NVSMI_COUNT in filter)):
            nvidia_smi_results['count'] = deviceCount
        for i in range(0, deviceCount):
            gpuResults = {}
            handle = self.__handles[i]
            pciInfo = nvmlDeviceGetPciInfo(handle)
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_BUS_ID in filter)):
                gpuResults['id'] = nvidia_smi.__toString(pciInfo.busId)
            if ((NVSMI_ALL in filter) or (NVSMI_NAME in filter)):
                gpuResults['product_name'] = nvidia_smi.__toString(nvmlDeviceGetName(handle))
                try:
                    brandName = NVSMI_BRAND_NAMES[nvmlDeviceGetBrand(handle)]
                except NVMLError as err:
                    brandName = nvidia_smi.__handleError(err)
                gpuResults['product_brand'] = brandName
            if ((NVSMI_ALL in filter) or (NVSMI_DISPLAY_MODE in filter)):
                try:
                    state = ('Enabled' if (nvmlDeviceGetDisplayMode(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    state = nvidia_smi.__handleError(err)
                gpuResults['display_mode'] = state
            if ((NVSMI_ALL in filter) or (NVSMI_DISPLAY_ACTIVE in filter)):
                try:
                    state = ('Enabled' if (nvmlDeviceGetDisplayActive(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    state = nvidia_smi.__handleError(err)
                gpuResults['display_active'] = state
            if ((NVSMI_ALL in filter) or (NVSMI_PERSISTENCE_MODE in filter)):
                try:
                    mode = ('Enabled' if (nvmlDeviceGetPersistenceMode(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    mode = nvidia_smi.__handleError(err)
                gpuResults['persistence_mode'] = mode
            migMode = {}
            includeMigMode = False
            if ((NVSMI_ALL in filter) or (NVSMI_MIG_MODE_CURRENT in filter) or (NVSMI_MIG_MODE_PENDING in filter)):
                try:
                    (current, pending) = nvmlDeviceGetMigMode(handle)
                except NVMLError as err:
                    current = nvidia_smi.__handleError(err)
                    pending = current
                migMode['current_mm'] = ('Enabled' if (current == NVML_DEVICE_MIG_ENABLE) else 'Disabled')
                migMode['pending_mm'] = ('Enabled' if (pending == NVML_DEVICE_MIG_ENABLE) else 'Disabled')
                includeMigMode = True
            if includeMigMode:
                gpuResults['mig_mode'] = migMode
            if ((NVSMI_ALL in filter) or (NVSMI_ACCT_MODE in filter)):
                try:
                    mode = ('Enabled' if (nvmlDeviceGetAccountingMode(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    mode = nvidia_smi.__handleError(err)
                gpuResults['accounting_mode'] = mode
            if ((NVSMI_ALL in filter) or (NVSMI_ACCT_BUFFER_SIZE in filter)):
                try:
                    bufferSize = nvidia_smi.__toString(nvmlDeviceGetAccountingBufferSize(handle))
                except NVMLError as err:
                    bufferSize = nvidia_smi.__handleError(err)
                gpuResults['accounting_mode_buffer_size'] = bufferSize
            driverModel = {}
            includeDriverModel = False
            if ((NVSMI_ALL in filter) or (NVSMI_DRIVER_MODEL_CUR in filter)):
                try:
                    current = ('WDDM' if (nvmlDeviceGetCurrentDriverModel(handle) == NVML_DRIVER_WDDM) else 'TCC')
                except NVMLError as err:
                    current = nvidia_smi.__handleError(err)
                driverModel['current_dm'] = current
                includeDriverModel = True
            if ((NVSMI_ALL in filter) or (NVSMI_DRIVER_MODEL_PENDING in filter)):
                try:
                    pending = ('WDDM' if (nvmlDeviceGetPendingDriverModel(handle) == NVML_DRIVER_WDDM) else 'TCC')
                except NVMLError as err:
                    pending = nvidia_smi.__handleError(err)
                driverModel['pending_dm'] = pending
                includeDriverModel = True
            if includeDriverModel:
                gpuResults['driver_model'] = driverModel
            if ((NVSMI_ALL in filter) or (NVSMI_SERIALNUMBER in filter)):
                try:
                    serial = nvmlDeviceGetSerial(handle)
                except NVMLError as err:
                    serial = nvidia_smi.__handleError(err)
                gpuResults['serial'] = nvidia_smi.__toString(serial)
            if ((NVSMI_ALL in filter) or (NVSMI_UUID in filter)):
                try:
                    uuid = nvmlDeviceGetUUID(handle)
                except NVMLError as err:
                    uuid = nvidia_smi.__handleError(err)
                gpuResults['uuid'] = nvidia_smi.__toString(uuid)
            if ((NVSMI_ALL in filter) or (NVSMI_INDEX in filter)):
                try:
                    minor_number = nvmlDeviceGetMinorNumber(handle)
                except NVMLError as err:
                    minor_number = nvidia_smi.__handleError(err)
                gpuResults['minor_number'] = nvidia_smi.__toString(minor_number)
            if ((NVSMI_ALL in filter) or (NVSMI_VBIOS_VER in filter)):
                try:
                    vbios = nvmlDeviceGetVbiosVersion(handle)
                except NVMLError as err:
                    vbios = nvidia_smi.__handleError(err)
                gpuResults['vbios_version'] = nvidia_smi.__toString(vbios)
            if ((NVSMI_ALL in filter) or (NVSMI_VBIOS_VER in filter)):
                try:
                    multiGpuBool = nvmlDeviceGetMultiGpuBoard(handle)
                except NVMLError as err:
                    multiGpuBool = nvidia_smi.__handleError(err)
                if (multiGpuBool == 'N/A'):
                    gpuResults['multigpu_board'] = 'N/A'
                elif multiGpuBool:
                    gpuResults['multigpu_board'] = 'Yes'
                else:
                    gpuResults['multigpu_board'] = 'No'
            if ((NVSMI_ALL in filter) or (NVSMI_BOARD_ID in filter)):
                try:
                    boardId = nvmlDeviceGetBoardId(handle)
                except NVMLError as err:
                    boardId = nvidia_smi.__handleError(err)
                try:
                    hexBID = ('0x%x' % boardId)
                except:
                    hexBID = boardId
                gpuResults['board_id'] = hexBID
            inforomVersion = {}
            includeInforom = False
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_IMG in filter)):
                try:
                    img = nvmlDeviceGetInforomImageVersion(handle)
                except NVMLError as err:
                    img = nvidia_smi.__handleError(err)
                inforomVersion['img_version'] = nvidia_smi.__toString(img)
                includeInforom = True
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_OEM in filter)):
                try:
                    oem = nvmlDeviceGetInforomVersion(handle, NVML_INFOROM_OEM)
                except NVMLError as err:
                    oem = nvidia_smi.__handleError(err)
                inforomVersion['oem_object'] = nvidia_smi.__toString(oem)
                includeInforom = True
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_ECC in filter)):
                try:
                    ecc = nvmlDeviceGetInforomVersion(handle, NVML_INFOROM_ECC)
                except NVMLError as err:
                    ecc = nvidia_smi.__handleError(err)
                inforomVersion['ecc_object'] = nvidia_smi.__toString(ecc)
                includeInforom = True
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_PWR in filter)):
                try:
                    pwr = nvmlDeviceGetInforomVersion(handle, NVML_INFOROM_POWER)
                except NVMLError as err:
                    pwr = nvidia_smi.__handleError(err)
                inforomVersion['pwr_object'] = nvidia_smi.__toString(pwr)
                includeInforom = True
            if includeInforom:
                gpuResults['inforom_version'] = inforomVersion
            gpuOperationMode = {}
            includeGOM = False
            if ((NVSMI_ALL in filter) or (NVSMI_GOM_CUR in filter)):
                try:
                    current = nvidia_smi.__toStrGOM(nvmlDeviceGetCurrentGpuOperationMode(handle))
                except NVMLError as err:
                    current = nvidia_smi.__handleError(err)
                gpuOperationMode['current_gom'] = nvidia_smi.__toString(current)
                includeGOM = True
            if ((NVSMI_ALL in filter) or (NVSMI_GOM_PENDING in filter)):
                try:
                    pending = nvidia_smi.__toStrGOM(nvmlDeviceGetPendingGpuOperationMode(handle))
                except NVMLError as err:
                    pending = nvidia_smi.__handleError(err)
                gpuOperationMode['pending_gom'] = nvidia_smi.__toString(pending)
                includeGOM = True
            if includeGOM:
                gpuResults['gpu_operation_mode'] = gpuOperationMode
            pci = {}
            includePci = False
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_BUS in filter)):
                pci['pci_bus'] = ('%02X' % pciInfo.bus)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_DEVICE in filter)):
                pci['pci_device'] = ('%02X' % pciInfo.device)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_DOMAIN in filter)):
                pci['pci_domain'] = ('%04X' % pciInfo.domain)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_DEVICE_ID in filter)):
                pci['pci_device_id'] = ('%08X' % pciInfo.pciDeviceId)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_BUS_ID in filter)):
                pci['pci_bus_id'] = nvidia_smi.__toString(pciInfo.busId)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_SUBDEVICE_ID in filter)):
                pci['pci_sub_system_id'] = ('%08X' % pciInfo.pciSubSystemId)
                includePci = True
            pciGpuLinkInfo = {}
            includeLinkInfo = False
            pciGen = {}
            includeGen = False
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_GEN_MAX in filter)):
                try:
                    gen = nvidia_smi.__toString(nvmlDeviceGetMaxPcieLinkGeneration(handle))
                except NVMLError as err:
                    gen = nvidia_smi.__handleError(err)
                pciGen['max_link_gen'] = gen
                includeGen = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_GEN_CUR in filter)):
                try:
                    gen = nvidia_smi.__toString(nvmlDeviceGetCurrPcieLinkGeneration(handle))
                except NVMLError as err:
                    gen = nvidia_smi.__handleError(err)
                pciGen['current_link_gen'] = gen
                includeGen = True
            if includeGen:
                pciGpuLinkInfo['pcie_gen'] = pciGen
                includeLinkInfo = True
            pciLinkWidths = {}
            includeLinkWidths = False
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_WIDTH_MAX in filter)):
                try:
                    width = (nvidia_smi.__toString(nvmlDeviceGetMaxPcieLinkWidth(handle)) + 'x')
                except NVMLError as err:
                    width = nvidia_smi.__handleError(err)
                pciLinkWidths['max_link_width'] = width
                includeLinkWidths = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_WIDTH_CUR in filter)):
                try:
                    width = (nvidia_smi.__toString(nvmlDeviceGetCurrPcieLinkWidth(handle)) + 'x')
                except NVMLError as err:
                    width = nvidia_smi.__handleError(err)
                pciLinkWidths['current_link_width'] = width
                includeLinkWidths = True
            if includeLinkWidths:
                pciGpuLinkInfo['link_widths'] = pciLinkWidths
                includeLinkInfo = True
            if includeLinkInfo:
                pci['pci_gpu_link_info'] = pciGpuLinkInfo
                includePci = True
            pciBridgeChip = {}
            includeBridgeChip = False
            if (NVSMI_ALL in filter):
                try:
                    bridgeHierarchy = nvmlDeviceGetBridgeChipInfo(handle)
                    bridge_type = ''
                    if (bridgeHierarchy.bridgeChipInfo[0].type == 0):
                        bridge_type += 'PLX'
                    else:
                        bridge_type += 'BR04'
                    pciBridgeChip['bridge_chip_type'] = bridge_type
                    if (bridgeHierarchy.bridgeChipInfo[0].fwVersion == 0):
                        strFwVersion = 'N/A'
                    else:
                        strFwVersion = ('%08X' % bridgeHierarchy.bridgeChipInfo[0].fwVersion)
                    pciBridgeChip['bridge_chip_fw'] = nvidia_smi.__toString(strFwVersion)
                except NVMLError as err:
                    pciBridgeChip['bridge_chip_type'] = nvidia_smi.__handleError(err)
                    pciBridgeChip['bridge_chip_fw'] = nvidia_smi.__handleError(err)
                includeBridgeChip = True
            if includeBridgeChip:
                pci['pci_bridge_chip'] = pciBridgeChip
                includePci = True
            if (NVSMI_ALL in filter):
                try:
                    replay = nvmlDeviceGetPcieReplayCounter(handle)
                    pci['replay_counter'] = nvidia_smi.__toString(replay)
                except NVMLError as err:
                    pci['replay_counter'] = nvidia_smi.__handleError(err)
                includePci = True
            if (NVSMI_ALL in filter):
                try:
                    tx_bytes = nvmlDeviceGetPcieThroughput(handle, NVML_PCIE_UTIL_TX_BYTES)
                    pci['tx_util'] = tx_bytes
                    pci['tx_util_unit'] = 'KB/s'
                except NVMLError as err:
                    pci['tx_util'] = nvidia_smi.__handleError(err)
                includePci = True
            if (NVSMI_ALL in filter):
                try:
                    rx_bytes = nvmlDeviceGetPcieThroughput(handle, NVML_PCIE_UTIL_RX_BYTES)
                    pci['rx_util'] = rx_bytes
                    pci['rx_util_unit'] = 'KB/s'
                except NVMLError as err:
                    pci['rx_util'] = nvidia_smi.__handleError(err)
                includePci = True
            if includePci:
                gpuResults['pci'] = pci
            if ((NVSMI_ALL in filter) or (NVSMI_FAN_SPEED in filter)):
                try:
                    fan = nvmlDeviceGetFanSpeed(handle)
                except NVMLError as err:
                    fan = nvidia_smi.__handleError(err)
                gpuResults['fan_speed'] = fan
                gpuResults['fan_speed_unit'] = '%'
            if ((NVSMI_ALL in filter) or (NVSMI_PSTATE in filter)):
                try:
                    perfState = nvmlDeviceGetPowerState(handle)
                    perfStateStr = ('P%s' % perfState)
                except NVMLError as err:
                    perfStateStr = nvidia_smi.__handleError(err)
                gpuResults['performance_state'] = perfStateStr
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SUPPORTED in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_ACTIVE in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_IDLE in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_APP_SETTING in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SW_PWR_CAP in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_HW_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_HW_THERMAL_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_HW_PWR_BRAKE_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SW_THERMAL_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SYNC_BOOST in filter)):
                gpuResults['clocks_throttle'] = nvidia_smi.__GetClocksThrottleReasons(handle)
            fbMemoryUsage = {}
            includeMemoryUsage = False
            if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_TOTAL in filter) or (NVSMI_MEMORY_USED in filter) or (NVSMI_MEMORY_FREE in filter)):
                includeMemoryUsage = True
                try:
                    memInfo = nvmlDeviceGetMemoryInfo(handle)
                    mem_total = ((memInfo.total / 1024) / 1024)
                    mem_used = ((memInfo.used / 1024) / 1024)
                    mem_free = (((memInfo.total / 1024) / 1024) - ((memInfo.used / 1024) / 1024))
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    mem_total = error
                    mem_used = error
                    mem_free = error
                if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_TOTAL in filter)):
                    fbMemoryUsage['total'] = mem_total
                if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_USED in filter)):
                    fbMemoryUsage['used'] = mem_used
                if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_FREE in filter)):
                    fbMemoryUsage['free'] = mem_free
            if includeMemoryUsage:
                fbMemoryUsage['unit'] = 'MiB'
                gpuResults['fb_memory_usage'] = fbMemoryUsage
            if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_BAR1 in filter)):
                try:
                    memInfo = nvmlDeviceGetBAR1MemoryInfo(handle)
                    mem_total = ((memInfo.bar1Total / 1024) / 1024)
                    mem_used = ((memInfo.bar1Used / 1024) / 1024)
                    mem_free = (((memInfo.bar1Total / 1024) / 1024) - ((memInfo.bar1Used / 1024) / 1024))
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    mem_total = error
                    mem_used = error
                    mem_free = error
                bar1MemoryUsage = {}
                bar1MemoryUsage['total'] = mem_total
                bar1MemoryUsage['used'] = mem_used
                bar1MemoryUsage['free'] = mem_free
                bar1MemoryUsage['unit'] = 'MiB'
                gpuResults['bar1_memory_usage'] = bar1MemoryUsage
            if ((NVSMI_ALL in filter) or (NVSMI_COMPUTE_MODE in filter)):
                try:
                    mode = nvmlDeviceGetComputeMode(handle)
                    if (mode == NVML_COMPUTEMODE_DEFAULT):
                        modeStr = 'Default'
                    elif (mode == NVML_COMPUTEMODE_EXCLUSIVE_THREAD):
                        modeStr = 'Exclusive Thread'
                    elif (mode == NVML_COMPUTEMODE_PROHIBITED):
                        modeStr = 'Prohibited'
                    elif (mode == NVML_COMPUTEMODE_EXCLUSIVE_PROCESS):
                        modeStr = 'Exclusive_Process'
                    else:
                        modeStr = 'Unknown'
                except NVMLError as err:
                    modeStr = nvidia_smi.__handleError(err)
                gpuResults['compute_mode'] = modeStr
            utilization = {}
            includeUtilization = False
            if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_GPU in filter) or (NVSMI_UTILIZATION_MEM in filter)):
                try:
                    util = nvmlDeviceGetUtilizationRates(handle)
                    gpu_util = util.gpu
                    mem_util = util.memory
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    gpu_util = error
                    mem_util = error
                if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_GPU in filter)):
                    utilization['gpu_util'] = gpu_util
                if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_MEM in filter)):
                    utilization['memory_util'] = mem_util
                includeUtilization = True
            if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_ENCODER in filter)):
                try:
                    (util_int, ssize) = nvmlDeviceGetEncoderUtilization(handle)
                    encoder_util = util_int
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    encoder_util = error
                utilization['encoder_util'] = encoder_util
                includeUtilization = True
            if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_DECODER in filter)):
                try:
                    (util_int, ssize) = nvmlDeviceGetDecoderUtilization(handle)
                    decoder_util = util_int
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    decoder_util = error
                utilization['decoder_util'] = decoder_util
                includeUtilization = True
            if includeUtilization:
                utilization['unit'] = '%'
                gpuResults['utilization'] = utilization
            if ((NVSMI_ALL in filter) or (NVSMI_ECC_MODE_CUR in filter) or (NVSMI_ECC_MODE_PENDING in filter)):
                try:
                    (current, pending) = nvmlDeviceGetEccMode(handle)
                    curr_str = ('Enabled' if (current != 0) else 'Disabled')
                    pend_str = ('Enabled' if (pending != 0) else 'Disabled')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    curr_str = error
                    pend_str = error
                eccMode = {}
                if ((NVSMI_ALL in filter) or (NVSMI_ECC_MODE_CUR in filter)):
                    eccMode['current_ecc'] = curr_str
                if ((NVSMI_ALL in filter) or (NVSMI_ECC_MODE_PENDING in filter)):
                    eccMode['pending_ecc'] = pend_str
                gpuResults['ecc_mode'] = eccMode
            (eccErrors, includeEccErrors) = nvidia_smi.__GetEcc(handle, filter)
            if includeEccErrors:
                gpuResults['ecc_errors'] = eccErrors
            (retiredPages, includeRetiredPages) = nvidia_smi.__GetRetiredPages(handle, filter)
            if includeRetiredPages:
                gpuResults['retired_pages'] = retiredPages
            temperature = {}
            includeTemperature = False
            if ((NVSMI_ALL in filter) or (NVSMI_TEMPERATURE_GPU in filter)):
                try:
                    temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
                except NVMLError as err:
                    temp = nvidia_smi.__handleError(err)
                temperature['gpu_temp'] = temp
                includeTemperature = True
                try:
                    temp = nvmlDeviceGetTemperatureThreshold(handle, NVML_TEMPERATURE_THRESHOLD_SHUTDOWN)
                except NVMLError as err:
                    temp = nvidia_smi.__handleError(err)
                temperature['gpu_temp_max_threshold'] = temp
                includeTemperature = True
                try:
                    temp = nvmlDeviceGetTemperatureThreshold(handle, NVML_TEMPERATURE_THRESHOLD_SLOWDOWN)
                except NVMLError as err:
                    temp = nvidia_smi.__handleError(err)
                temperature['gpu_temp_slow_threshold'] = temp
                includeTemperature = True
            if includeTemperature:
                temperature['unit'] = 'C'
                gpuResults['temperature'] = temperature
            power_readings = {}
            includePowerReadings = False
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_MGMT in filter)):
                try:
                    powMan = nvmlDeviceGetPowerManagementMode(handle)
                    powManStr = ('Supported' if (powMan != 0) else 'N/A')
                except NVMLError as err:
                    powManStr = nvidia_smi.__handleError(err)
                power_readings['power_management'] = powManStr
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_DRAW in filter)):
                try:
                    powDraw = (nvmlDeviceGetPowerUsage(handle) / 1000.0)
                    powDrawStr = powDraw
                except NVMLError as err:
                    powDrawStr = nvidia_smi.__handleError(err)
                power_readings['power_draw'] = powDrawStr
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT in filter)):
                try:
                    powLimit = (nvmlDeviceGetPowerManagementLimit(handle) / 1000.0)
                    powLimitStr = powLimit
                except NVMLError as err:
                    powLimitStr = nvidia_smi.__handleError(err)
                power_readings['power_limit'] = powLimitStr
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_DEFAULT in filter)):
                try:
                    powLimit = (nvmlDeviceGetPowerManagementDefaultLimit(handle) / 1000.0)
                    powLimitStr = powLimit
                except NVMLError as err:
                    powLimitStr = nvidia_smi.__handleError(err)
                power_readings['default_power_limit'] = powLimitStr
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_ENFORCED in filter)):
                try:
                    enforcedPowLimit = (nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0)
                    enforcedPowLimitStr = enforcedPowLimit
                except NVMLError as err:
                    enforcedPowLimitStr = nvidia_smi.__handleError(err)
                power_readings['enforced_power_limit'] = enforcedPowLimitStr
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_MIN in filter) or (NVSMI_POWER_LIMIT_MAX in filter)):
                try:
                    powLimit = nvmlDeviceGetPowerManagementLimitConstraints(handle)
                    powLimitStrMin = (powLimit[0] / 1000.0)
                    powLimitStrMax = (powLimit[1] / 1000.0)
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    powLimitStrMin = error
                    powLimitStrMax = error
                if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_MIN in filter)):
                    power_readings['min_power_limit'] = powLimitStrMin
                if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_MAX in filter)):
                    power_readings['max_power_limit'] = powLimitStrMax
                includePowerReadings = True
            if includePowerReadings:
                try:
                    perfState = ('P' + nvidia_smi.__toString(nvmlDeviceGetPowerState(handle)))
                except NVMLError as err:
                    perfState = nvidia_smi.__handleError(err)
                power_readings['power_state'] = perfState
                power_readings['unit'] = 'W'
                gpuResults['power_readings'] = power_readings
            clocks = {}
            includeClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_GRAPHICS_CUR in filter)):
                try:
                    graphics = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                clocks['graphics_clock'] = graphics
                includeClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_GRAPHICS_CUR in filter)):
                try:
                    sm = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM)
                except NVMLError as err:
                    sm = nvidia_smi.__handleError(err)
                clocks['sm_clock'] = sm
                includeClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_MEMORY_CUR in filter)):
                try:
                    mem = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                clocks['mem_clock'] = mem
                includeClocks = True
            if includeClocks:
                clocks['unit'] = 'MHz'
                gpuResults['clocks'] = clocks
            applicationClocks = {}
            includeAppClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_GRAPHICS in filter)):
                try:
                    graphics = nvmlDeviceGetApplicationsClock(handle, NVML_CLOCK_GRAPHICS)
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                applicationClocks['graphics_clock'] = graphics
                includeAppClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_MEMORY in filter)):
                try:
                    mem = nvmlDeviceGetApplicationsClock(handle, NVML_CLOCK_MEM)
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                applicationClocks['mem_clock'] = mem
                includeAppClocks = True
            if includeAppClocks:
                applicationClocks['unit'] = 'MHz'
                gpuResults['applications_clocks'] = applicationClocks
            defaultApplicationClocks = {}
            includeDefaultAppClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_GRAPHICS_DEFAULT in filter)):
                try:
                    graphics = nvmlDeviceGetDefaultApplicationsClock(handle, NVML_CLOCK_GRAPHICS)
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                defaultApplicationClocks['graphics_clock'] = graphics
                includeDefaultAppClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_MEMORY_DEFAULT in filter)):
                try:
                    mem = nvmlDeviceGetDefaultApplicationsClock(handle, NVML_CLOCK_MEM)
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                defaultApplicationClocks['mem_clock'] = mem
                includeDefaultAppClocks = True
            if includeDefaultAppClocks:
                defaultApplicationClocks['unit'] = 'MHz'
                gpuResults['default_applications_clocks'] = defaultApplicationClocks
            maxClocks = {}
            includeMaxClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_GRAPHICS_MAX in filter)):
                try:
                    graphics = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_GRAPHICS)
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                maxClocks['graphics_clock'] = graphics
                includeMaxClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_SM_MAX in filter)):
                try:
                    sm = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_SM)
                except NVMLError as err:
                    sm = nvidia_smi.__handleError(err)
                maxClocks['sm_clock'] = sm
                includeMaxClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_MEMORY_MAX in filter)):
                try:
                    mem = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_MEM)
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                maxClocks['mem_clock'] = mem
                includeMaxClocks = True
            if includeMaxClocks:
                maxClocks['unit'] = 'MHz'
                gpuResults['max_clocks'] = maxClocks
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_POLICY in filter)):
                clockPolicy = {}
                try:
                    (boostedState, boostedDefaultState) = nvmlDeviceGetAutoBoostedClocksEnabled(handle)
                    if (boostedState == NVML_FEATURE_DISABLED):
                        autoBoostStr = 'Off'
                    else:
                        autoBoostStr = 'On'
                    if (boostedDefaultState == NVML_FEATURE_DISABLED):
                        autoBoostDefaultStr = 'Off'
                    else:
                        autoBoostDefaultStr = 'On'
                except NVMLError_NotSupported:
                    autoBoostStr = 'N/A'
                    autoBoostDefaultStr = 'N/A'
                except NVMLError as err:
                    autoBoostStr = nvidia_smi.__handleError(err)
                    autoBoostDefaultStr = nvidia_smi.__handleError(err)
                clockPolicy['auto_boost'] = autoBoostStr
                clockPolicy['auto_boost_default'] = autoBoostDefaultStr
                gpuResults['clock_policy'] = clockPolicy
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_SUPPORTED in filter)):
                supportedClocks = []
                try:
                    memClocks = nvmlDeviceGetSupportedMemoryClocks(handle)
                    for m in memClocks:
                        supportMemClock = {}
                        supportMemClock['current'] = m
                        supportMemClock['unit'] = 'MHz'
                        supportedGraphicsClocks = []
                        try:
                            clocks = nvmlDeviceGetSupportedGraphicsClocks(handle, m)
                            for c in clocks:
                                supportedGraphicsClocks.append(c)
                        except NVMLError as err:
                            supportedGraphicsClocks = nvidia_smi.__handleError(err)
                        supportMemClock['supported_graphics_clock'] = supportedGraphicsClocks
                        supportedClocks.append(supportMemClock)
                except NVMLError as err:
                    supportedClocks['Error'] = nvidia_smi.__handleError(err)
                gpuResults['supported_clocks'] = (supportedClocks if (len(supportedClocks) > 0) else None)
            if ((NVSMI_ALL in filter) or (NVSMI_COMPUTE_APPS in filter)):
                processes = []
                try:
                    procs = nvmlDeviceGetComputeRunningProcesses(handle)
                    for p in procs:
                        try:
                            name = nvidia_smi.__toString(nvmlSystemGetProcessName(p.pid))
                        except NVMLError as err:
                            if (err.value == NVML_ERROR_NOT_FOUND):
                                continue
                            else:
                                name = nvidia_smi.__handleError(err)
                        processInfo = {}
                        processInfo['pid'] = p.pid
                        processInfo['process_name'] = name
                        if (p.usedGpuMemory == None):
                            mem = 0
                        else:
                            mem = int(((p.usedGpuMemory / 1024) / 1024))
                        processInfo['used_memory'] = mem
                        processInfo['unit'] = 'MiB'
                        processes.append(processInfo)
                except NVMLError as err:
                    processes = nvidia_smi.__handleError(err)
                gpuResults['processes'] = (processes if (len(processes) > 0) else None)
            if ((NVSMI_ALL in filter) or (NVSMI_ACCOUNTED_APPS in filter)):
                try:
                    pids = nvmlDeviceGetAccountingPids(handle)
                    accountProcess = []
                    for pid in pids:
                        try:
                            stats = nvmlDeviceGetAccountingStats(handle, pid)
                            gpuUtilization = ('%d %%' % stats.gpuUtilization)
                            memoryUtilization = ('%d %%' % stats.memoryUtilization)
                            if (stats.maxMemoryUsage == None):
                                maxMemoryUsage = 'N/A'
                            else:
                                maxMemoryUsage = ('%d MiB' % ((stats.maxMemoryUsage / 1024) / 1024))
                            time = ('%d ms' % stats.time)
                            is_running = ('%d' % stats.isRunning)
                        except NVMLError as err:
                            if (err.value == NVML_ERROR_NOT_FOUND):
                                continue
                            err = nvidia_smi.__handleError(err)
                            gpuUtilization = err
                            memoryUtilization = err
                            maxMemoryUsage = err
                            time = err
                            is_running = err
                        accountProcessInfo = {}
                        accountProcessInfo['pid'] = ('%d' % pid)
                        accountProcessInfo['gpu_util'] = gpuUtilization
                        accountProcessInfo['memory_util'] = memoryUtilization
                        accountProcessInfo['max_memory_usage'] = maxMemoryUsage
                        accountProcessInfo['time'] = time
                        accountProcessInfo['is_running'] = is_running
                        accountProcess.append(accountProcessInfo)
                    gpuResults['accounted_processes'] = (accountProcess if (len(accountProcess) > 0) else None)
                except NVMLError as err:
                    gpuResults['accounted_processes'] = nvidia_smi.__handleError(err)
            if (len(gpuResults) > 0):
                dictResult.append(gpuResults)
        if (len(dictResult) > 0):
            nvidia_smi_results['gpu'] = dictResult
    except NVMLError as err:
        print((('nvidia_smi.py: ' + err.__str__()) + '\n'))
    return nvidia_smi_results
