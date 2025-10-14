
package org.playmetric.model;

public record DeviceDetails(
    String deviceId,
    String deviceModel,
    String osVersion,
    String platform,
    String appVersion
) {}
