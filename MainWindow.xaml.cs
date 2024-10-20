using System.Windows;
using System.Windows.Media;
using MediaDevices;
using Microsoft.Win32;

namespace QuickCameraImporter;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    public static MainWindow mainWindow;
    public static DeviceLink deviceLink = new();
    OpenFolderDialog folderDialog = new();
    String path = "";
    
        
    // STARTUP LOGIC
    
    public MainWindow()
    {
        InitializeComponent();
        mainWindow = this;
        CheckCamera();
    }

    private void CheckCamera()
    {
        var camera = deviceLink.FindCamera();
        string statusDisplay;
        if (camera!= null)
        {
            statusDisplay = camera.Manufacturer + " " + camera.FriendlyName;
            cameraStatus.Text = statusDisplay;
            cameraStatus.Foreground = Brushes.LimeGreen;
        }
        else
        {
            statusDisplay = "No Camera Found";
            cameraStatus.Text = statusDisplay;
            cameraStatus.Foreground = Brushes.Orange;
        }
    }
    
    // GUI EVENTS

    private void OnClick_BtnCopy(object sender, RoutedEventArgs e)
    {
        Console.WriteLine("Clicked");
    }

    private void OnCLick_BtnBrowse(object sender, RoutedEventArgs e)
    {
        if (folderDialog.ShowDialog() != true) return;
        var folderName = folderDialog.FolderName;
        // Do something with the result
        Console.WriteLine("got a file " + folderName);
        PathDisplay.Text = folderName;
    }

    private void OnCLick_BtnCheck(object sender, RoutedEventArgs e)
    {
        CheckCamera();
    }
}