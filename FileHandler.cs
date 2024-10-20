using System.IO;
using MediaDevices;

namespace QuickCameraImporter;

public class FileHandler
{
    public void CopyFiles(MediaDevice camera, string destination)
    {
        Console.WriteLine("Attempting to back up " + camera.Manufacturer +" "+ camera.FriendlyName + " to " + destination);

        var allFiles = camera.GetRootDirectory().EnumerateFiles("*.*", SearchOption.AllDirectories);
        
        // works but is also slow
        foreach (var file in allFiles)
        {
            MemoryStream memoryStream = new MemoryStream();
            camera.DownloadFile(file.FullName, memoryStream);
            memoryStream.Position = 0;
            var fileWithPath = Path.Combine(destination, file.Name);
            WriteSreamToDisk(fileWithPath, memoryStream);
        }
        
        // // works but is slow
        // foreach (var file in allFiles)
        // {
        //     MemoryStream memoryStream = new System.IO.MemoryStream();
        //     camera.DownloadFile(file.FullName, memoryStream);
        //     memoryStream.Position = 0;
        //     var fileWithPath = Path.Combine(destination, file.Name);
        //     WriteSreamToDisk(fileWithPath, memoryStream);
        // }
    }
    
    static void WriteSreamToDisk(string filePath, MemoryStream memoryStream)
    {
        using (FileStream file = new FileStream(filePath, FileMode.Create, System.IO.FileAccess.Write))
        {
            byte[] bytes = new byte[memoryStream.Length];
            memoryStream.Read(bytes, 0, (int)memoryStream.Length);
            file.Write(bytes, 0, bytes.Length);
            memoryStream.Close();
        }
    }
}