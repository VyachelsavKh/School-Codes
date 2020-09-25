using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Automation.Peers;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace TicTacToe
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public int[] Cells = new int[9];
        public int[] Players = new int[2];

        int nowPlayer;
        int startPlayer;

        public void init()
        {
            for (int i = 0; i < 9; i++)
            {
                Cells[i] = 0;
            }

            for (int i = 0; i < 2; i++)
            {
                Players[i] = 0;
            }

            nowPlayer = 1;
            startPlayer = 1;

            print();
        }

        public int checkWinner()
        {
            for (int i = 0; i <= 6; i += 3)
                if (Cells[i] == Cells[i + 1] && Cells[i] == Cells[i + 2] && Cells[i] != 0)
                    return Cells[i];

            for (int i = 0; i < 3; i++)
                if (Cells[i] == Cells[i + 3] && Cells[i] == Cells[i + 6] && Cells[i] != 0)
                    return Cells[i];

            if (Cells[0] == Cells[4] && Cells[0] == Cells[8] && Cells[0] != 0)
                return Cells[0];

            if (Cells[2] == Cells[4] && Cells[2] == Cells[6] && Cells[2] != 0)
                return Cells[2];

            if (Cells[0] != 0 && Cells[1] != 0 && Cells[2] != 0 && Cells[3] != 0 && Cells[4] != 0 && Cells[5] != 0 && Cells[6] != 0 && Cells[7] != 0 && Cells[8] != 0)
                return -1;

            return 0;
        }

        public void print()
        {
            BT1.Text = Cells[0] == 0 ? "" : Cells[0] == 1 ? "X" : "O";
            BT2.Text = Cells[1] == 0 ? "" : Cells[1] == 1 ? "X" : "O";
            BT3.Text = Cells[2] == 0 ? "" : Cells[2] == 1 ? "X" : "O";
            BT4.Text = Cells[3] == 0 ? "" : Cells[3] == 1 ? "X" : "O";
            BT5.Text = Cells[4] == 0 ? "" : Cells[4] == 1 ? "X" : "O";
            BT6.Text = Cells[5] == 0 ? "" : Cells[5] == 1 ? "X" : "O";
            BT7.Text = Cells[6] == 0 ? "" : Cells[6] == 1 ? "X" : "O";
            BT8.Text = Cells[7] == 0 ? "" : Cells[7] == 1 ? "X" : "O";
            BT9.Text = Cells[8] == 0 ? "" : Cells[8] == 1 ? "X" : "O";

            Fig.Text = nowPlayer == 1 ? "X" : "O";

            PL1.Text = Players[0].ToString();
            PL2.Text = Players[1].ToString();
        }

        public void pressButton(int bt)
        {
            if (bt == 9)
            {
                init();
                return;
            }

            if (Cells[bt] != 0)
                return;

            Cells[bt] = nowPlayer;

            if (nowPlayer == 1)
                nowPlayer = 2;
            else
                nowPlayer = 1;

            int winner = checkWinner();

            if (winner != 0)
            {
                if (winner != -1)
                    Players[winner - 1]++;

                if (startPlayer == 1)
                    startPlayer = 2;
                else
                    startPlayer = 1;

                nowPlayer = startPlayer;

                for (int i = 0; i < 9; i++)
                {
                    Cells[i] = 0;
                }
            }

            print();
        }

        public MainWindow()
        {
            InitializeComponent();
            init();
        }

        private void Button_Click(object sender, RoutedEventArgs e)   //0 0
        {
            pressButton(0);
        }

        private void Button_Click_1(object sender, RoutedEventArgs e) //0 1
        {
            pressButton(1);
        }

        private void Button_Click_2(object sender, RoutedEventArgs e) //0 2
        {
            pressButton(2);
        }

        private void Button_Click_3(object sender, RoutedEventArgs e) //1 0
        {
            pressButton(3);
        }

        private void Button_Click_4(object sender, RoutedEventArgs e) //1 1
        {
            pressButton(4);
        }

        private void Button_Click_5(object sender, RoutedEventArgs e) //1 2
        {
            pressButton(5);
        }

        private void Button_Click_6(object sender, RoutedEventArgs e) //2 0
        {
            pressButton(6);
        }

        private void Button_Click_7(object sender, RoutedEventArgs e) //2 1
        {
            pressButton(7);
        }

        private void Button_Click_8(object sender, RoutedEventArgs e) //2 2
        {
            pressButton(8);
        }

        private void Button_Click_9(object sender, RoutedEventArgs e) //Reset
        {
            pressButton(9);
        }
    }
}
