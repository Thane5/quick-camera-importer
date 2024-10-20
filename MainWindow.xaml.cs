using System.IO;
using System.Windows;
using System.Windows.Controls;
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
    public static FileHandler fileHandler = new();
    OpenFolderDialog folderDialog = new();

    private MediaDevice? camera;
    String path = "";
    
        
    // STARTUP LOGIC
    
    public MainWindow()
    {
        InitializeComponent();
        mainWindow = this;

        LoadSettings();
        CheckConditions();
    }

    private bool CameraOkay()
    {
        camera = deviceLink.FindCamera();
        string statusDisplay;
        if (camera!= null)
        {
            statusDisplay = camera.Manufacturer + " " + camera.FriendlyName;
            CameraStatus.Text = statusDisplay;
            CameraStatus.Foreground = Brushes.LimeGreen;
            return true;    
        }

        statusDisplay = "No Camera Found";
        CameraStatus.Text = statusDisplay;
        CameraStatus.Foreground = Brushes.Orange;
        return false;
    }

    private bool PathOkay()
    {
        if (Directory.Exists(PathDisplay.Text))
        {
            path = PathDisplay.Text;
            return true;
        }
        return false;
    }

    private bool CheckConditions()
    {
        if (CameraOkay() && PathOkay())
        {
            BtnCopy.IsEnabled = true;
            return true;
        }
        BtnCopy.IsEnabled = false;
        return false;
    }

    private void LoadSettings()
    {
        // Todo: load settings from file
        if (true)
        {
            PathDisplay.Text = Environment.GetFolderPath(Environment.SpecialFolder.MyPictures);
        }
    }
    
    // GUI EVENTS

    private void OnClick_BtnCopy(object sender, RoutedEventArgs e)
    {
        if (CheckConditions())
        {
            fileHandler.CopyFiles(camera, path);
        }
        else
        {
            Console.WriteLine("Unable to copy files.");
        }
    }

    private void OnCLick_BtnBrowse(object sender, RoutedEventArgs e)
    {
        folderDialog.DefaultDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyPictures);
        // Todo: load the last path and set the InitialDirectory here
        //folderDialog.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyPictures);
        if (PathOkay())
        {
            folderDialog.InitialDirectory = path;
        }
        
        if (folderDialog.ShowDialog() != true) return;
        var folderName = folderDialog.FolderName;
        Console.WriteLine("got a file " + folderName);
        PathDisplay.Text = folderName;
    }

    private void OnCLick_BtnCheck(object sender, RoutedEventArgs e)
    {
        CheckConditions();
    }

    private void OnChange_PathDisplay(object sender, TextChangedEventArgs e)
    {
        CheckConditions();
    }
}