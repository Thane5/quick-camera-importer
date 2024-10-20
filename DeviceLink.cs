using MediaDevices;

namespace QuickCameraImporter;

public class DeviceLink
{
    public MediaDevice? FindCamera()
    {
        // native api
        // IPortableDeviceManager manager = new PortableDeviceManager();
        // manager.RefreshDeviceList();
        // manager.GetDevices();
        // Console.WriteLine(manager.PortableDevices.First().DeviceFriendlyName);
        
        //--------------------------------------------------
        var devices = MediaDevice.GetDevices();
        List<MediaDevice> cameras = [];
        
        // If no devices are found, return
        if (!devices.Any())
        {
            Console.WriteLine("No Devices found");
            return null;
        }
        
        foreach (MediaDevice device in devices)
        {
            // Connect to the device
            device.Connect();
            
            // Check if it is a camera
            if (device.DeviceType == DeviceType.Camera)
            {
                Console.WriteLine("Found Camera: " + device.Manufacturer +" "+ device.FriendlyName);
                cameras.Add(device);
            }
        }
        
        // If no cameras are found, return
        if (!cameras.Any())
        {
            Console.WriteLine("No cameras found");
            return null;
        }
        
        // Return the first camera as the current camera
        Console.WriteLine("Selected Camera: " + cameras.First().Manufacturer +" "+ cameras.First().FriendlyName);
        return cameras.First();
    }
}