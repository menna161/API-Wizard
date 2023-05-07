from pynvml.nvml import *
import datetime
import collections
import time
from threading import Thread


@classmethod
def XmlDeviceQuery(self, filter=None):
    '\n      Provides a Python interface to GPU management and monitoring functions.\n\n      This is a wrapper around the NVML library.\n      For information about the NVML library, see the NVML developer page\n      http://developer.nvidia.com/nvidia-management-library-nvml\n\n      Examples:\n      ---------------------------------------------------------------------------\n      For all elements as in XML format.  Similiar to nvisia-smi -q -x\n\n      $ XmlDeviceQuery()\n\n      ---------------------------------------------------------------------------\n      For XML of filtered elements by string name.\n      Similiar ot nvidia-smi --query-gpu=pci.bus_id,memory.total,memory.free\n      See help_query_gpu.txt or XmlDeviceQuery("--help-query-gpu") for available filter elements\n\n      $ XmlDeviceQuery("pci.bus_id,memory.total,memory.free")\n\n      ---------------------------------------------------------------------------\n      For XML of filtered elements by enumeration value.\n      See help_query_gpu.txt or XmlDeviceQuery("--help_query_gpu") for available filter elements\n\n      $ XmlDeviceQuery([NVSMI_PCI_BUS_ID, NVSMI_MEMORY_TOTAL, NVSMI_MEMORY_FREE])\n\n      '
    if (filter is None):
        filter = [NVSMI_ALL]
    elif isinstance(filter, str):
        if ((filter == '--help') or (filter == '-h')):
            return nvidia_smi.XmlDeviceQuery.__doc__
        elif (filter == '--help-query-gpu'):
            with open('help_query_gpu.txt', 'r') as fin:
                return fin.read()
        else:
            filter = nvidia_smi.__fromDeviceQueryString(filter)
    else:
        filter = list(filter)
    strResult = ''
    try:
        strResult += '<?xml version="1.0" ?>\n'
        strResult += '<!DOCTYPE nvidia_smi_log SYSTEM "nvsmi_device_v4.dtd">\n'
        strResult += '<nvidia_smi>\n'
        if ((NVSMI_ALL in filter) or (NVSMI_TIMESTAMP in filter)):
            strResult += (('  <timestamp>' + nvidia_smi.__toString(datetime.date.today())) + '</timestamp>\n')
        if ((NVSMI_ALL in filter) or (NVSMI_DRIVER_VERSION in filter)):
            strResult += (('  <driver_version>' + nvidia_smi.__toString(nvmlSystemGetDriverVersion())) + '</driver_version>\n')
        deviceCount = nvmlDeviceGetCount()
        if ((NVSMI_ALL in filter) or (NVSMI_COUNT in filter)):
            strResult += (('  <count>' + nvidia_smi.__toString(deviceCount)) + '</count>\n')
        for i in range(0, deviceCount):
            handle = self.__handles[i]
            pciInfo = nvmlDeviceGetPciInfo(handle)
            gpuInfo = ''
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_BUS_ID in filter)):
                gpuInfo += ('  <id>%s</id>\n' % pciInfo.busId)
            if ((NVSMI_ALL in filter) or (NVSMI_NAME in filter)):
                gpuInfo += (('    <product_name>' + nvidia_smi.__toString(nvmlDeviceGetName(handle))) + '</product_name>\n')
                try:
                    brandName = NVSMI_BRAND_NAMES[nvmlDeviceGetBrand(handle)]
                except NVMLError as err:
                    brandName = nvidia_smi.__handleError(err)
                gpuInfo += (('    <product_brand>' + brandName) + '</product_brand>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_DISPLAY_MODE in filter)):
                try:
                    state = ('Enabled' if (nvmlDeviceGetDisplayMode(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    state = nvidia_smi.__handleError(err)
                gpuInfo += (('    <display_mode>' + state) + '</display_mode>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_DISPLAY_ACTIVE in filter)):
                try:
                    state = ('Enabled' if (nvmlDeviceGetDisplayActive(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    state = nvidia_smi.__handleError(err)
                gpuInfo += (('    <display_active>' + state) + '</display_active>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_PERSISTENCE_MODE in filter)):
                try:
                    mode = ('Enabled' if (nvmlDeviceGetPersistenceMode(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    mode = nvidia_smi.__handleError(err)
                gpuInfo += (('    <persistence_mode>' + mode) + '</persistence_mode>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_ACCT_MODE in filter)):
                try:
                    mode = ('Enabled' if (nvmlDeviceGetAccountingMode(handle) != 0) else 'Disabled')
                except NVMLError as err:
                    mode = nvidia_smi.__handleError(err)
                gpuInfo += (('    <accounting_mode>' + mode) + '</accounting_mode>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_ACCT_BUFFER_SIZE in filter)):
                try:
                    bufferSize = nvidia_smi.__toString(nvmlDeviceGetAccountingBufferSize(handle))
                except NVMLError as err:
                    bufferSize = nvidia_smi.__handleError(err)
                gpuInfo += (('    <accounting_mode_buffer_size>' + bufferSize) + '</accounting_mode_buffer_size>\n')
            migMode = ''
            includeMigMode = False
            if ((NVSMI_ALL in filter) or (NVSMI_MIG_MODE_CURRENT in filter) or (NVSMI_MIG_MODE_PENDING in filter)):
                try:
                    (current, pending) = nvmlDeviceGetMigMode(handle)
                    current = ('Enabled' if (current == NVML_DEVICE_MIG_ENABLE) else 'Disabled')
                    pending = ('Enabled' if (pending == NVML_DEVICE_MIG_ENABLE) else 'Disabled')
                except NVMLError as err:
                    current = nvidia_smi.__handleError(err)
                    pending = current
                migMode += (('      <current_mm>' + current) + '</current_mm>\n')
                migMode += (('      <pending_mm>' + pending) + '</pending_mm>\n')
                includeMigMode = True
            if includeMigMode:
                gpuInfo += '    <mig_mode>\n'
                gpuInfo += migMode
                gpuInfo += '    </mig_mode>\n'
            driverModel = ''
            includeDriverModel = False
            if ((NVSMI_ALL in filter) or (NVSMI_DRIVER_MODEL_CUR in filter)):
                try:
                    current = ('WDDM' if (nvmlDeviceGetCurrentDriverModel(handle) == NVML_DRIVER_WDDM) else 'TCC')
                except NVMLError as err:
                    current = nvidia_smi.__handleError(err)
                driverModel += (('      <current_dm>' + current) + '</current_dm>\n')
                includeDriverModel = True
            if ((NVSMI_ALL in filter) or (NVSMI_DRIVER_MODEL_PENDING in filter)):
                try:
                    pending = ('WDDM' if (nvmlDeviceGetPendingDriverModel(handle) == NVML_DRIVER_WDDM) else 'TCC')
                except NVMLError as err:
                    pending = nvidia_smi.__handleError(err)
                    driverModel += (('      <pending_dm>' + pending) + '</pending_dm>\n')
                    includeDriverModel = True
            if includeDriverModel:
                gpuInfo += '    <driver_model>\n'
                gpuInfo += driverModel
                gpuInfo += '    </driver_model>\n'
            if ((NVSMI_ALL in filter) or (NVSMI_SERIALNUMBER in filter)):
                try:
                    serial = nvmlDeviceGetSerial(handle)
                except NVMLError as err:
                    serial = nvidia_smi.__handleError(err)
                gpuInfo += (('    <serial>' + nvidia_smi.__toString(serial)) + '</serial>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_UUID in filter)):
                try:
                    uuid = nvmlDeviceGetUUID(handle)
                except NVMLError as err:
                    uuid = nvidia_smi.__handleError(err)
                gpuInfo += (('    <uuid>' + nvidia_smi.__toString(uuid)) + '</uuid>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_INDEX in filter)):
                try:
                    minor_number = nvmlDeviceGetMinorNumber(handle)
                except NVMLError as err:
                    minor_number = nvidia_smi.__handleError(err)
                gpuInfo += (('    <minor_number>' + nvidia_smi.__toString(minor_number)) + '</minor_number>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_VBIOS_VER in filter)):
                try:
                    vbios = nvmlDeviceGetVbiosVersion(handle)
                except NVMLError as err:
                    vbios = nvidia_smi.__handleError(err)
                gpuInfo += (('    <vbios_version>' + nvidia_smi.__toString(vbios)) + '</vbios_version>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_VBIOS_VER in filter)):
                try:
                    multiGpuBool = nvmlDeviceGetMultiGpuBoard(handle)
                except NVMLError as err:
                    multiGpuBool = nvidia_smi.__handleError(err)
                if (multiGpuBool == 'N/A'):
                    gpuInfo += (('    <multigpu_board>' + 'N/A') + '</multigpu_board>\n')
                elif multiGpuBool:
                    gpuInfo += (('    <multigpu_board>' + 'Yes') + '</multigpu_board>\n')
                else:
                    gpuInfo += (('    <multigpu_board>' + 'No') + '</multigpu_board>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_BOARD_ID in filter)):
                try:
                    boardId = nvmlDeviceGetBoardId(handle)
                except NVMLError as err:
                    boardId = nvidia_smi.__handleError(err)
                try:
                    hexBID = ('0x%x' % boardId)
                except:
                    hexBID = boardId
                gpuInfo += (('    <board_id>' + hexBID) + '</board_id>\n')
            inforomVersion = ''
            includeInforom = False
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_IMG in filter)):
                try:
                    img = nvmlDeviceGetInforomImageVersion(handle)
                except NVMLError as err:
                    img = nvidia_smi.__handleError(err)
                inforomVersion += (('      <img_version>' + nvidia_smi.__toString(img)) + '</img_version>\n')
                includeInforom = True
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_OEM in filter)):
                try:
                    oem = nvmlDeviceGetInforomVersion(handle, NVML_INFOROM_OEM)
                except NVMLError as err:
                    oem = nvidia_smi.__handleError(err)
                inforomVersion += (('      <oem_object>' + nvidia_smi.__toString(oem)) + '</oem_object>\n')
                includeInforom = True
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_ECC in filter)):
                try:
                    ecc = nvmlDeviceGetInforomVersion(handle, NVML_INFOROM_ECC)
                except NVMLError as err:
                    ecc = nvidia_smi.__handleError(err)
                inforomVersion += (('      <ecc_object>' + nvidia_smi.__toString(ecc)) + '</ecc_object>\n')
                includeInforom = True
            if ((NVSMI_ALL in filter) or (NVSMI_INFOROM_PWR in filter)):
                try:
                    pwr = nvmlDeviceGetInforomVersion(handle, NVML_INFOROM_POWER)
                except NVMLError as err:
                    pwr = nvidia_smi.__handleError(err)
                inforomVersion += (('      <pwr_object>' + nvidia_smi.__toString(pwr)) + '</pwr_object>\n')
                includeInforom = True
            if includeInforom:
                gpuInfo += '    <inforom_version>\n'
                gpuInfo += inforomVersion
                gpuInfo += '    </inforom_version>\n'
            gpuOperationMode = ''
            includeGOM = False
            if ((NVSMI_ALL in filter) or (NVSMI_GOM_CUR in filter)):
                try:
                    current = nvidia_smi.__toStrGOM(nvmlDeviceGetCurrentGpuOperationMode(handle))
                except NVMLError as err:
                    current = nvidia_smi.__handleError(err)
                gpuOperationMode += (('      <current_gom>' + nvidia_smi.__toString(current)) + '</current_gom>\n')
                includeGOM = True
            if ((NVSMI_ALL in filter) or (NVSMI_GOM_PENDING in filter)):
                try:
                    pending = nvidia_smi.__toStrGOM(nvmlDeviceGetPendingGpuOperationMode(handle))
                except NVMLError as err:
                    pending = nvidia_smi.__handleError(err)
                gpuOperationMode += (('      <pending_gom>' + nvidia_smi.__toString(pending)) + '</pending_gom>\n')
                includeGOM = True
            if includeGOM:
                gpuInfo += '    <gpu_operation_mode>\n'
                gpuInfo += gpuOperationMode
                gpuInfo += '    </gpu_operation_mode>\n'
            pci = ''
            includePci = False
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_BUS in filter)):
                pci += ('      <pci_bus>%02X</pci_bus>\n' % pciInfo.bus)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_DEVICE in filter)):
                pci += ('      <pci_device>%02X</pci_device>\n' % pciInfo.device)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_DOMAIN in filter)):
                pci += ('      <pci_domain>%04X</pci_domain>\n' % pciInfo.domain)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_DEVICE_ID in filter)):
                pci += ('      <pci_device_id>%08X</pci_device_id>\n' % pciInfo.pciDeviceId)
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_BUS_ID in filter)):
                pci += (('      <pci_bus_id>' + nvidia_smi.__toString(pciInfo.busId)) + '</pci_bus_id>\n')
                includePci = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_SUBDEVICE_ID in filter)):
                pci += ('      <pci_sub_system_id>%08X</pci_sub_system_id>\n' % pciInfo.pciSubSystemId)
                includePci = True
            pciGpuLinkInfo = ''
            includeLinkInfo = False
            pciGen = ''
            includeGen = False
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_GEN_MAX in filter)):
                try:
                    gen = nvidia_smi.__toString(nvmlDeviceGetMaxPcieLinkGeneration(handle))
                except NVMLError as err:
                    gen = nvidia_smi.__handleError(err)
                pciGen += (('          <max_link_gen>' + gen) + '</max_link_gen>\n')
                includeGen = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_GEN_CUR in filter)):
                try:
                    gen = nvidia_smi.__toString(nvmlDeviceGetCurrPcieLinkGeneration(handle))
                except NVMLError as err:
                    gen = nvidia_smi.__handleError(err)
                pciGen += (('          <current_link_gen>' + gen) + '</current_link_gen>\n')
                includeGen = True
            if includeGen:
                pciGpuLinkInfo += '        <pcie_gen>\n'
                pciGpuLinkInfo += pciGen
                pciGpuLinkInfo += '        </pcie_gen>\n'
                includeLinkInfo = True
            pciLinkWidths = ''
            includeLinkWidths = False
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_WIDTH_MAX in filter)):
                try:
                    width = (nvidia_smi.__toString(nvmlDeviceGetMaxPcieLinkWidth(handle)) + 'x')
                except NVMLError as err:
                    width = nvidia_smi.__handleError(err)
                pciLinkWidths += (('          <max_link_width>' + width) + '</max_link_width>\n')
                includeLinkWidths = True
            if ((NVSMI_ALL in filter) or (NVSMI_PCI_LINK_WIDTH_CUR in filter)):
                try:
                    width = (nvidia_smi.__toString(nvmlDeviceGetCurrPcieLinkWidth(handle)) + 'x')
                except NVMLError as err:
                    width = nvidia_smi.__handleError(err)
                pciLinkWidths += (('          <current_link_width>' + width) + '</current_link_width>\n')
                includeLinkWidths = True
            if includeLinkWidths:
                pciGpuLinkInfo += '        <link_widths>\n'
                pciGpuLinkInfo += pciLinkWidths
                pciGpuLinkInfo += '        </link_widths>\n'
                includeLinkInfo = True
            if includeLinkInfo:
                pci += '      <pci_gpu_link_info>\n'
                pci += pciGpuLinkInfo
                pci += '      </pci_gpu_link_info>\n'
            pciBridgeChip = ''
            includeBridgeChip = False
            if (NVSMI_ALL in filter):
                try:
                    bridgeHierarchy = nvmlDeviceGetBridgeChipInfo(handle)
                    bridge_type = ''
                    if (bridgeHierarchy.bridgeChipInfo[0].type == 0):
                        bridge_type += 'PLX'
                    else:
                        bridge_type += 'BR04'
                    pciBridgeChip += (('        <bridge_chip_type>' + bridge_type) + '</bridge_chip_type>\n')
                    if (bridgeHierarchy.bridgeChipInfo[0].fwVersion == 0):
                        strFwVersion = 'N/A'
                    else:
                        strFwVersion = ('%08X' % bridgeHierarchy.bridgeChipInfo[0].fwVersion)
                    pciBridgeChip += ('        <bridge_chip_fw>%s</bridge_chip_fw>\n' % strFwVersion)
                except NVMLError as err:
                    pciBridgeChip += (('        <bridge_chip_type>' + nvidia_smi.__handleError(err)) + '</bridge_chip_type>\n')
                    pciBridgeChip += (('        <bridge_chip_fw>' + nvidia_smi.__handleError(err)) + '</bridge_chip_fw>\n')
                includeBridgeChip = True
            if includeBridgeChip:
                pci += '      <pci_bridge_chip>\n'
                pci += pciBridgeChip
                pci += '      </pci_bridge_chip>\n'
            if (NVSMI_ALL in filter):
                try:
                    replay = nvmlDeviceGetPcieReplayCounter(handle)
                    pci += (('      <replay_counter>' + nvidia_smi.__toString(replay)) + '</replay_counter>')
                except NVMLError as err:
                    pci += (('      <replay_counter>' + nvidia_smi.__handleError(err)) + '</replay_counter>')
                includePci = True
            if (NVSMI_ALL in filter):
                try:
                    tx_bytes = nvmlDeviceGetPcieThroughput(handle, NVML_PCIE_UTIL_TX_BYTES)
                    pci += ((('      <tx_util>' + nvidia_smi.__toString(tx_bytes)) + ' KB/s') + '</tx_util>')
                except NVMLError as err:
                    pci += (('      <tx_util>' + nvidia_smi.__handleError(err)) + '</tx_util>')
                includePci = True
            if (NVSMI_ALL in filter):
                try:
                    rx_bytes = nvmlDeviceGetPcieThroughput(handle, NVML_PCIE_UTIL_RX_BYTES)
                    pci += ((('      <rx_util>' + nvidia_smi.__toString(rx_bytes)) + ' KB/s') + '</rx_util>')
                except NVMLError as err:
                    pci += (('      <rx_util>' + nvidia_smi.__handleError(err)) + '</rx_util>')
                includePci = True
            if includePci:
                gpuInfo += '    <pci>\n'
                gpuInfo += pci
                gpuInfo += '    </pci>\n'
            if ((NVSMI_ALL in filter) or (NVSMI_FAN_SPEED in filter)):
                try:
                    fan = (nvidia_smi.__toString(nvmlDeviceGetFanSpeed(handle)) + ' %')
                except NVMLError as err:
                    fan = nvidia_smi.__handleError(err)
                gpuInfo += (('    <fan_speed>' + fan) + '</fan_speed>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_PSTATE in filter)):
                try:
                    perfState = nvmlDeviceGetPowerState(handle)
                    perfStateStr = ('P%s' % perfState)
                except NVMLError as err:
                    perfStateStr = nvidia_smi.__handleError(err)
                gpuInfo += (('    <performance_state>' + perfStateStr) + '</performance_state>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SUPPORTED in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_ACTIVE in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_IDLE in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_APP_SETTING in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SW_PWR_CAP in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_HW_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_HW_THERMAL_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_HW_PWR_BRAKE_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SW_THERMAL_SLOWDOWN in filter) or (NVSMI_CLOCK_THROTTLE_REASONS_SYNC_BOOST in filter)):
                gpuInfo += nvidia_smi.__xmlGetClocksThrottleReasons(handle)
            fbMemoryUsage = ''
            includeMemoryUsage = False
            if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_TOTAL in filter) or (NVSMI_MEMORY_USED in filter) or (NVSMI_MEMORY_FREE in filter)):
                includeMemoryUsage = True
                try:
                    memInfo = nvmlDeviceGetMemoryInfo(handle)
                    mem_total = (nvidia_smi.__toString(((memInfo.total / 1024) / 1024)) + ' MiB')
                    mem_used = (nvidia_smi.__toString(((memInfo.used / 1024) / 1024)) + ' MiB')
                    mem_free = (nvidia_smi.__toString((((memInfo.total / 1024) / 1024) - ((memInfo.used / 1024) / 1024))) + ' MiB')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    mem_total = error
                    mem_used = error
                    mem_free = error
                if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_TOTAL in filter)):
                    fbMemoryUsage += (('      <total>' + mem_total) + '</total>\n')
                if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_USED in filter)):
                    fbMemoryUsage += (('      <used>' + mem_used) + '</used>\n')
                if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_FREE in filter)):
                    fbMemoryUsage += (('      <free>' + mem_free) + '</free>\n')
            if includeMemoryUsage:
                gpuInfo += '    <fb_memory_usage>\n'
                gpuInfo += fbMemoryUsage
                gpuInfo += '    </fb_memory_usage>\n'
            if ((NVSMI_ALL in filter) or (NVSMI_MEMORY_BAR1 in filter)):
                try:
                    memInfo = nvmlDeviceGetBAR1MemoryInfo(handle)
                    mem_total = (nvidia_smi.__toString(((memInfo.bar1Total / 1024) / 1024)) + ' MiB')
                    mem_used = (nvidia_smi.__toString(((memInfo.bar1Used / 1024) / 1024)) + ' MiB')
                    mem_free = (nvidia_smi.__toString((((memInfo.bar1Total / 1024) / 1024) - ((memInfo.bar1Used / 1024) / 1024))) + ' MiB')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    mem_total = error
                    mem_used = error
                    mem_free = error
                gpuInfo += '    <bar1_memory_usage>\n'
                gpuInfo += (('      <total>' + mem_total) + '</total>\n')
                gpuInfo += (('      <used>' + mem_used) + '</used>\n')
                gpuInfo += (('      <free>' + mem_free) + '</free>\n')
                gpuInfo += '    </bar1_memory_usage>\n'
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
                gpuInfo += (('    <compute_mode>' + modeStr) + '</compute_mode>\n')
            utilization = ''
            includeUtilization = False
            if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_GPU in filter) or (NVSMI_UTILIZATION_MEM in filter)):
                try:
                    util = nvmlDeviceGetUtilizationRates(handle)
                    gpu_util = (nvidia_smi.__toString(util.gpu) + ' %')
                    mem_util = (nvidia_smi.__toString(util.memory) + ' %')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    gpu_util = error
                    mem_util = error
                if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_GPU in filter)):
                    utilization += (('      <gpu_util>' + gpu_util) + '</gpu_util>\n')
                if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_MEM in filter)):
                    utilization += (('      <memory_util>' + mem_util) + '</memory_util>\n')
                includeUtilization = True
            if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_ENCODER in filter)):
                try:
                    (util_int, ssize) = nvmlDeviceGetEncoderUtilization(handle)
                    encoder_util = (nvidia_smi.__toString(util_int) + ' %')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    encoder_util = error
                utilization += (('      <encoder_util>' + encoder_util) + '</encoder_util>\n')
                includeUtilization = True
            if ((NVSMI_ALL in filter) or (NVSMI_UTILIZATION_DECODER in filter)):
                try:
                    (util_int, ssize) = nvmlDeviceGetDecoderUtilization(handle)
                    decoder_util = (nvidia_smi.__toString(util_int) + ' %')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    decoder_util = error
                utilization += (('      <decoder_util>' + decoder_util) + '</decoder_util>\n')
                includeUtilization = True
            if includeUtilization:
                gpuInfo += '    <utilization>\n'
                gpuInfo += utilization
                gpuInfo += '    </utilization>\n'
            if ((NVSMI_ALL in filter) or (NVSMI_ECC_MODE_CUR in filter) or (NVSMI_ECC_MODE_PENDING in filter)):
                try:
                    (current, pending) = nvmlDeviceGetEccMode(handle)
                    curr_str = ('Enabled' if (current != 0) else 'Disabled')
                    pend_str = ('Enabled' if (pending != 0) else 'Disabled')
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    curr_str = error
                    pend_str = error
                eccMode = ''
                if ((NVSMI_ALL in filter) or (NVSMI_ECC_MODE_CUR in filter)):
                    eccMode += (('      <current_ecc>' + curr_str) + '</current_ecc>\n')
                if ((NVSMI_ALL in filter) or (NVSMI_ECC_MODE_PENDING in filter)):
                    eccMode += (('      <pending_ecc>' + pend_str) + '</pending_ecc>\n')
                gpuInfo += '    <ecc_mode>\n'
                gpuInfo += eccMode
                gpuInfo += '    </ecc_mode>\n'
            (eccErrors, includeEccErrors) = nvidia_smi.__xmlGetEcc(handle, filter)
            if includeEccErrors:
                gpuInfo += '    <ecc_errors>\n'
                gpuInfo += eccErrors
                gpuInfo += '    </ecc_errors>\n'
            (retiredPages, includeRetiredPages) = nvidia_smi.__xmlGetRetiredPages(handle, filter)
            if includeRetiredPages:
                gpuInfo += '    <retired_pages>\n'
                gpuInfo += retiredPages
                gpuInfo += '    </retired_pages>\n'
            temperature = ''
            includeTemperature = False
            if ((NVSMI_ALL in filter) or (NVSMI_TEMPERATURE_GPU in filter)):
                try:
                    temp = (nvidia_smi.__toString(nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)) + ' C')
                except NVMLError as err:
                    temp = nvidia_smi.__handleError(err)
                temperature += (('      <gpu_temp>' + temp) + '</gpu_temp>\n')
                try:
                    temp = (nvidia_smi.__toString(nvmlDeviceGetTemperatureThreshold(handle, NVML_TEMPERATURE_THRESHOLD_SHUTDOWN)) + ' C')
                except NVMLError as err:
                    temp = nvidia_smi.__handleError(err)
                temperature += (('      <gpu_temp_max_threshold>' + temp) + '</gpu_temp_max_threshold>\n')
                includeTemperature = True
                try:
                    temp = (nvidia_smi.__toString(nvmlDeviceGetTemperatureThreshold(handle, NVML_TEMPERATURE_THRESHOLD_SLOWDOWN)) + ' C')
                except NVMLError as err:
                    temp = nvidia_smi.__handleError(err)
                temperature += (('      <gpu_temp_slow_threshold>' + temp) + '</gpu_temp_slow_threshold>\n')
                includeTemperature = True
            if includeTemperature:
                gpuInfo += '    <temperature>\n'
                (gpuInfo + temperature)
                gpuInfo += '    </temperature>\n'
            power_readings = ''
            includePowerReadings = False
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_MGMT in filter)):
                try:
                    powMan = nvmlDeviceGetPowerManagementMode(handle)
                    powManStr = ('Supported' if (powMan != 0) else 'N/A')
                except NVMLError as err:
                    powManStr = nvidia_smi.__handleError(err)
                power_readings += (('      <power_management>' + powManStr) + '</power_management>\n')
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_DRAW in filter)):
                try:
                    powDraw = (nvmlDeviceGetPowerUsage(handle) / 1000.0)
                    powDrawStr = ('%.2f W' % powDraw)
                except NVMLError as err:
                    powDrawStr = nvidia_smi.__handleError(err)
                power_readings += (('      <power_draw>' + powDrawStr) + '</power_draw>\n')
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT in filter)):
                try:
                    powLimit = (nvmlDeviceGetPowerManagementLimit(handle) / 1000.0)
                    powLimitStr = ('%.2f W' % powLimit)
                except NVMLError as err:
                    powLimitStr = nvidia_smi.__handleError(err)
                power_readings += (('      <power_limit>' + powLimitStr) + '</power_limit>\n')
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_DEFAULT in filter)):
                try:
                    powLimit = (nvmlDeviceGetPowerManagementDefaultLimit(handle) / 1000.0)
                    powLimitStr = ('%.2f W' % powLimit)
                except NVMLError as err:
                    powLimitStr = nvidia_smi.__handleError(err)
                power_readings += (('      <default_power_limit>' + powLimitStr) + '</default_power_limit>\n')
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_ENFORCED in filter)):
                try:
                    enforcedPowLimit = (nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0)
                    enforcedPowLimitStr = ('%.2f W' % enforcedPowLimit)
                except NVMLError as err:
                    enforcedPowLimitStr = nvidia_smi.__handleError(err)
                power_readings += (('      <enforced_power_limit>' + enforcedPowLimitStr) + '</enforced_power_limit>\n')
                includePowerReadings = True
            if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_MIN in filter) or (NVSMI_POWER_LIMIT_MAX in filter)):
                try:
                    powLimit = nvmlDeviceGetPowerManagementLimitConstraints(handle)
                    powLimitStrMin = ('%.2f W' % (powLimit[0] / 1000.0))
                    powLimitStrMax = ('%.2f W' % (powLimit[1] / 1000.0))
                except NVMLError as err:
                    error = nvidia_smi.__handleError(err)
                    powLimitStrMin = error
                    powLimitStrMax = error
                if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_MIN in filter)):
                    power_readings += (('      <min_power_limit>' + powLimitStrMin) + '</min_power_limit>\n')
                if ((NVSMI_ALL in filter) or (NVSMI_POWER_LIMIT_MAX in filter)):
                    power_readings += (('      <max_power_limit>' + powLimitStrMax) + '</max_power_limit>\n')
                includePowerReadings = True
            if includePowerReadings:
                gpuInfo += '    <power_readings>\n'
                try:
                    perfState = ('P' + nvidia_smi.__toString(nvmlDeviceGetPowerState(handle)))
                except NVMLError as err:
                    perfState = nvidia_smi.__handleError(err)
                gpuInfo += ('      <power_state>%s</power_state>\n' % perfState)
                gpuInfo += power_readings
                gpuInfo += '    </power_readings>\n'
            clocks = ''
            includeClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_GRAPHICS_CUR in filter)):
                try:
                    graphics = (nvidia_smi.__toString(nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)) + ' MHz')
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                clocks += (('      <graphics_clock>' + graphics) + '</graphics_clock>\n')
                includeClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_GRAPHICS_CUR in filter)):
                try:
                    sm = (nvidia_smi.__toString(nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM)) + ' MHz')
                except NVMLError as err:
                    sm = nvidia_smi.__handleError(err)
                clocks += (('      <sm_clock>' + sm) + '</sm_clock>\n')
                includeClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_MEMORY_CUR in filter)):
                try:
                    mem = (nvidia_smi.__toString(nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)) + ' MHz')
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                clocks += (('      <mem_clock>' + mem) + '</mem_clock>\n')
                includeClocks = True
            if includeClocks:
                gpuInfo += '    <clocks>\n'
                gpuInfo += clocks
                gpuInfo += '    </clocks>\n'
            applicationClocks = ''
            includeAppClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_GRAPHICS in filter)):
                try:
                    graphics = (nvidia_smi.__toString(nvmlDeviceGetApplicationsClock(handle, NVML_CLOCK_GRAPHICS)) + ' MHz')
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                applicationClocks += (('      <graphics_clock>' + graphics) + '</graphics_clock>\n')
                includeAppClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_MEMORY in filter)):
                try:
                    mem = (nvidia_smi.__toString(nvmlDeviceGetApplicationsClock(handle, NVML_CLOCK_MEM)) + ' MHz')
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                applicationClocks += (('      <mem_clock>' + mem) + '</mem_clock>\n')
                includeAppClocks = True
            if includeAppClocks:
                gpuInfo += '    <applications_clocks>\n'
                gpuInfo += applicationClocks
                gpuInfo += '    </applications_clocks>\n'
            defaultApplicationClocks = ''
            includeDefaultAppClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_GRAPHICS_DEFAULT in filter)):
                try:
                    graphics = (nvidia_smi.__toString(nvmlDeviceGetDefaultApplicationsClock(handle, NVML_CLOCK_GRAPHICS)) + ' MHz')
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                defaultApplicationClocks += (('      <graphics_clock>' + graphics) + '</graphics_clock>\n')
                includeDefaultAppClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_APPL_MEMORY_DEFAULT in filter)):
                try:
                    mem = (nvidia_smi.__toString(nvmlDeviceGetDefaultApplicationsClock(handle, NVML_CLOCK_MEM)) + ' MHz')
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                defaultApplicationClocks += (('      <mem_clock>' + mem) + '</mem_clock>\n')
                includeDefaultAppClocks = True
            if includeDefaultAppClocks:
                gpuInfo += '    <default_applications_clocks>\n'
                gpuInfo += defaultApplicationClocks
                gpuInfo += '    </default_applications_clocks>\n'
            maxClocks = ''
            includeMaxClocks = False
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_GRAPHICS_MAX in filter)):
                try:
                    graphics = (nvidia_smi.__toString(nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_GRAPHICS)) + ' MHz')
                except NVMLError as err:
                    graphics = nvidia_smi.__handleError(err)
                maxClocks += (('      <graphics_clock>' + graphics) + '</graphics_clock>\n')
                includeMaxClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_SM_MAX in filter)):
                try:
                    sm = (nvidia_smi.__toString(nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_SM)) + ' MHz')
                except NVMLError as err:
                    sm = nvidia_smi.__handleError(err)
                maxClocks += (('      <sm_clock>' + sm) + '</sm_clock>\n')
                includeMaxClocks = True
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_MEMORY_MAX in filter)):
                try:
                    mem = (nvidia_smi.__toString(nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_MEM)) + ' MHz')
                except NVMLError as err:
                    mem = nvidia_smi.__handleError(err)
                maxClocks += (('      <mem_clock>' + mem) + '</mem_clock>\n')
                includeMaxClocks = True
            if includeMaxClocks:
                gpuInfo += '    <max_clocks>\n'
                gpuInfo += maxClocks
                gpuInfo += '    </max_clocks>\n'
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_POLICY in filter)):
                gpuInfo += '    <clock_policy>\n'
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
                    pass
                gpuInfo += (('      <auto_boost>' + autoBoostStr) + '</auto_boost>\n')
                gpuInfo += (('      <auto_boost_default>' + autoBoostDefaultStr) + '</auto_boost_default>\n')
                gpuInfo += '    </clock_policy>\n'
            if ((NVSMI_ALL in filter) or (NVSMI_CLOCKS_SUPPORTED in filter)):
                try:
                    memClocks = nvmlDeviceGetSupportedMemoryClocks(handle)
                    gpuInfo += '    <supported_clocks>\n'
                    for m in memClocks:
                        gpuInfo += '      <supported_mem_clock>\n'
                        gpuInfo += ('        <value>%d MHz</value>\n' % m)
                        try:
                            clocks = nvmlDeviceGetSupportedGraphicsClocks(handle, m)
                            for c in clocks:
                                gpuInfo += ('        <supported_graphics_clock>%d MHz</supported_graphics_clock>\n' % c)
                        except NVMLError as err:
                            gpuInfo += ('        <supported_graphics_clock>%s</supported_graphics_clock>\n' % nvidia_smi.__handleError(err))
                        gpuInfo += '      </supported_mem_clock>\n'
                    gpuInfo += '    </supported_clocks>\n'
                except NVMLError as err:
                    gpuInfo += (('    <supported_clocks>' + nvidia_smi.__handleError(err)) + '</supported_clocks>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_COMPUTE_APPS in filter)):
                try:
                    procs = nvmlDeviceGetComputeRunningProcesses(handle)
                    gpuInfo += '    <processes>\n'
                    for p in procs:
                        try:
                            name = nvidia_smi.__toString(nvmlSystemGetProcessName(p.pid))
                        except NVMLError as err:
                            if (err.value == NVML_ERROR_NOT_FOUND):
                                continue
                            else:
                                name = nvidia_smi.__handleError(err)
                        gpuInfo += '    <process_info>\n'
                        gpuInfo += ('      <pid>%d</pid>\n' % p.pid)
                        gpuInfo += (('      <process_name>' + name) + '</process_name>\n')
                        if (p.usedGpuMemory == None):
                            mem = 'N/A'
                        else:
                            mem = ('%d MiB' % ((p.usedGpuMemory / 1024) / 1024))
                        gpuInfo += (('      <used_memory>' + mem) + '</used_memory>\n')
                        gpuInfo += '    </process_info>\n'
                    gpuInfo += '    </processes>\n'
                except NVMLError as err:
                    gpuInfo += (('    <processes>' + nvidia_smi.__handleError(err)) + '</processes>\n')
            if ((NVSMI_ALL in filter) or (NVSMI_ACCOUNTED_APPS in filter)):
                try:
                    pids = nvmlDeviceGetAccountingPids(handle)
                    gpuInfo += '    <accounted_processes>\n'
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
                        gpuInfo += '    <accounted_process_info>\n'
                        gpuInfo += ('      <pid>%d</pid>\n' % pid)
                        gpuInfo += (('      <gpu_util>' + gpuUtilization) + '</gpu_util>\n')
                        gpuInfo += (('      <memory_util>' + memoryUtilization) + '</memory_util>\n')
                        gpuInfo += (('      <max_memory_usage>' + maxMemoryUsage) + '</max_memory_usage>\n')
                        gpuInfo += (('      <time>' + time) + '</time>\n')
                        gpuInfo += (('      <is_running>' + is_running) + '</is_running>\n')
                        gpuInfo += '    </accounted_process_info>\n'
                    gpuInfo += '    </accounted_processes>\n'
                except NVMLError as err:
                    gpuInfo += (('    <accounted_processes>' + nvidia_smi.__handleError(err)) + '</accounted_processes>\n')
            if (len(gpuInfo) > 0):
                strResult += '  <gpu>'
                strResult += gpuInfo
                strResult += '  </gpu>\n'
        strResult += '</nvidia_smi>\n'
    except NVMLError as err:
        strResult += (('nvidia_smi.py: ' + err.__str__()) + '\n')
    return strResult
