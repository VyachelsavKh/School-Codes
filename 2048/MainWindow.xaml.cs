using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace _2048
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        int[,] prevCells = new int[10000, 16];
        int turn;
        int score;
        int[] prevscore = new int[10000];

        public void init()
        {
            for (int i = 0; i < 1000; i++)
                for (int j = 0; j < 16; j++)
                    prevCells[i, j] = 0;

            turn = 0;
            score = 0;

            prevscore[turn] = score;

            generate();

            print();
        }

        public bool generate()
        {
            int free_count = 0;
            int[] free_cells = new int[16];

            for (int i = 0; i < 16; i++)
                if (prevCells[turn, i] == 0)
                {
                    free_cells[free_count] = i;
                    free_count++;
                }

            if (free_count == 0)
                return false;

            Random rnd = new Random();

            int cell = rnd.Next(0, free_count);

            int val = rnd.Next(1, 11);

            prevCells[turn, free_cells[cell]] = val == 10 ? 4 : 2;

            return true;
        }

        public void print()
        {
            C1.Text = prevCells[turn, 0] == 0 ? "" : prevCells[turn, 0].ToString();
            C2.Text = prevCells[turn, 1] == 0 ? "" : prevCells[turn, 1].ToString();
            C3.Text = prevCells[turn, 2] == 0 ? "" : prevCells[turn, 2].ToString();
            C4.Text = prevCells[turn, 3] == 0 ? "" : prevCells[turn, 3].ToString();
            C5.Text = prevCells[turn, 4] == 0 ? "" : prevCells[turn, 4].ToString();
            C6.Text = prevCells[turn, 5] == 0 ? "" : prevCells[turn, 5].ToString();
            C7.Text = prevCells[turn, 6] == 0 ? "" : prevCells[turn, 6].ToString();
            C8.Text = prevCells[turn, 7] == 0 ? "" : prevCells[turn, 7].ToString();
            C9.Text = prevCells[turn, 8] == 0 ? "" : prevCells[turn, 8].ToString();
            C10.Text = prevCells[turn, 9] == 0 ? "" : prevCells[turn, 9].ToString();
            C11.Text = prevCells[turn, 10] == 0 ? "" : prevCells[turn, 10].ToString();
            C12.Text = prevCells[turn, 11] == 0 ? "" : prevCells[turn, 11].ToString();
            C13.Text = prevCells[turn, 12] == 0 ? "" : prevCells[turn, 12].ToString();
            C14.Text = prevCells[turn, 13] == 0 ? "" : prevCells[turn, 13].ToString();
            C15.Text = prevCells[turn, 14] == 0 ? "" : prevCells[turn, 14].ToString();
            C16.Text = prevCells[turn, 15] == 0 ? "" : prevCells[turn, 15].ToString();

            Turns.Text = turn.ToString();

            Score.Text = score.ToString();
        }

        public bool moveLeft()
        {
            bool moved = false;

            for (int j = 0; j < 5; j++)
                for (int i = 0; i <= 12; i += 4)
                {
                    if (prevCells[turn, i + 2] == 0 && prevCells[turn, i + 3] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 2] = prevCells[turn, i + 3];
                        prevCells[turn, i + 3] = 0;
                    }

                    if (prevCells[turn, i + 1] == 0 && prevCells[turn, i + 2] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 1] = prevCells[turn, i + 2];
                        prevCells[turn, i + 2] = 0;
                    }

                    if (prevCells[turn, i] == 0 && prevCells[turn, i + 1] != 0)
                    {
                        moved = true;

                        prevCells[turn, i] = prevCells[turn, i + 1];
                        prevCells[turn, i + 1] = 0;
                    }

                }

            return moved;
        }

        public bool moveRight()
        {
            bool moved = false;

            for (int j = 0; j < 5; j++)
                for (int i = 0; i <= 12; i += 4)
                {
                    if (prevCells[turn, i + 3] == 0 && prevCells[turn, i + 2] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 3] = prevCells[turn, i + 2];
                        prevCells[turn, i + 2] = 0;
                    }

                    if (prevCells[turn, i + 2] == 0 && prevCells[turn, i + 1] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 2] = prevCells[turn, i + 1];
                        prevCells[turn, i + 1] = 0;
                    }

                    if (prevCells[turn, i + 1] == 0 && prevCells[turn, i] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 1] = prevCells[turn, i + 0];
                        prevCells[turn, i] = 0;
                    }

                }

            return moved;
        }

        public bool moveUp()
        {
            bool moved = false;

            for (int j = 0; j < 5; j++)
                for (int i = 0; i <= 3; i += 1)
                {
                    if (prevCells[turn, i + 8] == 0 && prevCells[turn, i + 12] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 8] = prevCells[turn, i + 12];
                        prevCells[turn, i + 12] = 0;
                    }

                    if (prevCells[turn, i + 4] == 0 && prevCells[turn, i + 8] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 4] = prevCells[turn, i + 8];
                        prevCells[turn, i + 8] = 0;
                    }

                    if (prevCells[turn, i] == 0 && prevCells[turn, i + 4] != 0)
                    {
                        moved = true;

                        prevCells[turn, i] = prevCells[turn, i + 4];
                        prevCells[turn, i + 4] = 0;
                    }

                }

            return moved;
        }

        public bool moveDown()
        {
            bool moved = false;

            for (int j = 0; j < 5; j++)
                for (int i = 0; i <= 3; i += 1)
                {
                    if (prevCells[turn, i + 12] == 0 && prevCells[turn, i + 8] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 12] = prevCells[turn, i + 8];
                        prevCells[turn, i + 8] = 0;
                    }

                    if (prevCells[turn, i + 8] == 0 && prevCells[turn, i + 4] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 8] = prevCells[turn, i + 4];
                        prevCells[turn, i + 4] = 0;
                    }

                    if (prevCells[turn, i + 4] == 0 && prevCells[turn, i] != 0)
                    {
                        moved = true;

                        prevCells[turn, i + 4] = prevCells[turn, i];
                        prevCells[turn, i] = 0;
                    }

                }

            return moved;
        }

        public int leftCollision()
        {
            int summ = 0;

            for (int i = 0; i <= 12; i += 4)
            {

                if (prevCells[turn, i] == prevCells[turn, i + 1] && prevCells[turn, i] != 0)
                {
                    summ += prevCells[turn, i] * 2;

                    prevCells[turn, i] *= 2;
                    prevCells[turn, i + 1] = 0;
                }

                if (prevCells[turn, i + 1] == prevCells[turn, i + 2] && prevCells[turn, i + 1] != 0)
                {
                    summ += prevCells[turn, i + 1] * 2;

                    prevCells[turn, i + 1] *= 2;
                    prevCells[turn, i + 2] = 0;
                }

                if (prevCells[turn, i + 2] == prevCells[turn, i + 3] && prevCells[turn, i + 2] != 0)
                {
                    summ += prevCells[turn, i + 2] * 2;

                    prevCells[turn, i + 2] *= 2;
                    prevCells[turn, i + 3] = 0;
                }
            }

            return summ;
        }

        public int rightCollision()
        {
            int summ = 0;

            for (int i = 0; i <= 12; i += 4)
            {
                if (prevCells[turn, i + 3] == prevCells[turn, i + 2] && prevCells[turn, i + 3] != 0)
                {
                    summ += prevCells[turn, i + 3] * 2;

                    prevCells[turn, i + 3] *= 2;
                    prevCells[turn, i + 2] = 0;
                }

                if (prevCells[turn, i + 2] == prevCells[turn, i + 1] && prevCells[turn, i + 2] != 0)
                {
                    summ += prevCells[turn, i + 2] * 2;

                    prevCells[turn, i + 2] *= 2;
                    prevCells[turn, i + 1] = 0;
                }

                if (prevCells[turn, i + 1] == prevCells[turn, i] && prevCells[turn, i + 1] != 0)
                {
                    summ += prevCells[turn, i + 1] * 2;

                    prevCells[turn, i + 1] *= 2;
                    prevCells[turn, i] = 0;
                }

            }

            return summ;
        }

        public int upCollision()
        {
            int summ = 0;

            for (int i = 0; i <= 3; i += 1)
            {
                if (prevCells[turn, i] == prevCells[turn, i + 4] && prevCells[turn, i + 4] != 0)
                {
                    summ += prevCells[turn, i] * 2;

                    prevCells[turn, i] *= 2;
                    prevCells[turn, i + 4] = 0;
                }

                if (prevCells[turn, i + 4] == prevCells[turn, i + 8] && prevCells[turn, i + 8] != 0)
                {
                    summ += prevCells[turn, i + 4] * 2;

                    prevCells[turn, i + 4] *= 2;
                    prevCells[turn, i + 8] = 0;
                }

                if (prevCells[turn, i + 8] == prevCells[turn, i + 12] && prevCells[turn, i + 8]  != 0)
                {
                    summ += prevCells[turn, i + 8] * 2;

                    prevCells[turn, i + 8] *= 2;
                    prevCells[turn, i + 12] = 0;
                }
            }

            return summ;
        }

        public int downCollision()
        {
            int summ = 0;

            for (int i = 0; i <= 3; i += 1)
            {
                if (prevCells[turn, i + 12] == prevCells[turn, i + 8] && prevCells[turn, i + 8] != 0)
                {
                    summ += prevCells[turn, i + 12] * 2;

                    prevCells[turn, i + 12] *= 2;
                    prevCells[turn, i + 8] = 0;
                }

                if (prevCells[turn, i + 8] == prevCells[turn, i + 4] && prevCells[turn, i + 4] != 0)
                {
                    summ += prevCells[turn, i + 8] * 2;

                    prevCells[turn, i + 8] *= 2;
                    prevCells[turn, i + 4] = 0;
                }

                if (prevCells[turn, i + 4] == prevCells[turn, i] && prevCells[turn, i] != 0)
                {
                    summ += prevCells[turn, i + 4] * 2;

                    prevCells[turn, i + 4] *= 2;
                    prevCells[turn, i] = 0;
                }

            }

            return summ;
        }

        public void btClick(int bt)
        {
            if (bt == 5)
            { 
                init();
                return;
            }

            else if (bt == 4)
            {
                turn--;

                score = prevscore[turn];

                if (turn < 0)
                    turn = 0;

                print();

                return;
            }

            for (int i = 0; i < 16; i++)
            {
                prevCells[turn + 1, i] = prevCells[turn, i];
            }

            turn++;

            bool moved = false;
            int summ = 0;

            if (bt == 0) //←
            {
                moved |= moveLeft();
                summ += leftCollision();
                moved |= moveLeft();
            }

            else if (bt == 1) //→
            {
                moved |= moveRight();
                summ += rightCollision();
                moved |= moveRight();
            }

            else if (bt == 2) //↑
            {
                moved |= moveUp();
                summ += upCollision();
                moved |= moveUp();

            }

            else if (bt == 3) //↓
            {
                moved |= moveDown();
                summ += downCollision();
                moved |= moveDown();
            }

            score += summ;

            prevscore[turn] = score;

            for(int i = 0; i < 16; i++)
                if(prevCells[turn, i] == 2048)
                    MessageBox.Show("You Win");


            if (!generate())
            {
                MessageBox.Show("You Lose");
                init();
            }

            if (!moved && summ == 0)
            {
                turn--;
                return;
            }

            print();
        }

        public MainWindow()
        {
            InitializeComponent();
            init();
        }

        private void Button_Click(object sender, RoutedEventArgs e) //←
        {
            btClick(0);
        }

        private void Button_Click_1(object sender, RoutedEventArgs e) //→
        {
            btClick(1);
        }

        private void Button_Click_2(object sender, RoutedEventArgs e) //↑
        {
            btClick(2);
        }

        private void Button_Click_3(object sender, RoutedEventArgs e) //↓
        {
            btClick(3);
        }


        private void Button_Click_5(object sender, RoutedEventArgs e) //⟲
        {
            btClick(4);
        }

        private void Button_Click_4(object sender, RoutedEventArgs e) //Restart
        {
            btClick(5);
        }
    }
}
