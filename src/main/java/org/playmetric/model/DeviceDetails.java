package org.playmetric.model;

import lombok.Data;

@Data
public class DeviceDetails {
    private String deviceId;
    private String deviceModel;
    private String osVersion;
    private String platform;
    private String appVersion;
}
