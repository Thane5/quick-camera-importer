using System.Windows;
using Microsoft.Win32;

namespace QuickCameraImporter;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    OpenFolderDialog folderDialog = new OpenFolderDialog();
    String path = "";
        
    public MainWindow()
    {
        InitializeComponent();
            
    }

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
        //throw new NotImplementedException();
    }
}