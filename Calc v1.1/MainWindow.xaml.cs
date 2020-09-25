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
using System.Windows.Media.TextFormatting;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Calc_v1._1
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            print();
        }

        public double a = 0;
        public string a_str = "0";

        public double b = 0;
        public string b_str = "";

        public string now_str = "";

        public bool inp_sign = false;
        public bool inp_b = false;

        public int sign = 0;

        public double prev = 0;

        public double mem = 0;
        public bool inp_mem = false;

        public bool error = false;

        public void print_memory()
        {
            if (inp_mem)
                mem_txt.Text = "M " + mem.ToString();
            else
                mem_txt.Text = "";
        }

        public void memory(int type)
        {
            switch (type)
            {
                case 0:
                    mem = 0;
                    inp_mem = false;
                    break;

                case 1:
                    if (error)
                        return;

                    if (inp_mem)
                    {
                        if (!inp_sign)
                        {
                            if (mem >= 0)
                            {
                                a = mem;
                            }
                            else
                            {
                                a = mem * -1;
                            }
                        }
                        else
                        {
                            if (mem >= 0)
                            {
                                b = mem;
                            }
                            else
                            {
                                b = mem * -1;
                            }

                            inp_b = true;
                        }
                    }

                    break;

                case 2:
                    if (error)
                        return;

                    if (!inp_b)
                        mem = a;
                    else
                        mem = b;

                    inp_mem = true;

                    break;

                case 3:
                    if (error)
                        return;

                    if (!inp_b)
                        mem += a;
                    else
                        mem += b;

                    inp_mem = true;

                    break;

                case 4:
                    if (error)
                        return;

                    if (!inp_b)
                        mem -= a;
                    else
                        mem -= b;

                    inp_mem = true;

                    break;

                default:
                    break;
            }

            print_memory();
            print();
        }

        public string print_num(string num, bool parentheses)
        {
            string str = "";

            if (num.Length != 0)
                if (Convert.ToDouble(num) < 0 && parentheses)
                    str += "(" + num + ")";
                else
                    str += num;

            return str;
        }

        public void print()
        {
            if (error)
            {
                txt.Text = "error";
                print_debug();
                return;
            }

            if (!inp_sign && !inp_b)
            {
                txt.Text = print_num(a_str, false);

                print_debug();

                return;
            }

            if (inp_sign && !inp_b)
            {
                if (a_str[a_str.Length - 1] == ',')
                    a_str = a_str.Remove(a_str.Length - 1);

                txt.Text = a_str + (sign == 0 ? " + " : sign == 1 ? " - " : sign == 2 ? " * " : " / ");

                print_debug();

                return;
            }

            if (inp_sign && inp_b)
            {
                txt.Text = a_str + (sign == 0 ? " + " : sign == 1 ? " - " : sign == 2 ? " * " : " / ") + print_num(b_str, true);

                print_debug();

                return;
            }
        }

        public void print_debug()
        {
            debug.Text = "Debug:\n"
                + "a " + a.ToString() + "\n"
                + "b " + b.ToString() + "\n"
                + "now_str " + now_str + "\n"
                + "a_str " + a_str + "\n"
                + "b_str " + b_str + "\n"
                + "inp_sign " + inp_sign.ToString() + "\n"
                + "inp_b " + inp_b.ToString() + "\n"
                + "sign " + sign.ToString() + "\n"
                + "prev " + prev.ToString() + "\n"
                + "mem " + mem.ToString() + "\n"
                + "inp_mem " + inp_mem.ToString() + "\n"
                + "error " + error.ToString() + "\n";
        }

        public void input_num(int num)
        {
            if (num <= 9)
            {
                if (error)
                    clear(0);

                if (now_str.Length == 1 && now_str[0] == '0')
                    now_str = "";

                if(now_str.Length <= 23)
                    now_str += num.ToString();

                if (!inp_sign)
                {
                    a_str = now_str;
                    a = Convert.ToDouble(now_str);
                }
                else
                {
                    b_str = now_str;
                    b = Convert.ToDouble(now_str);
                }

                if (inp_sign)
                    inp_b = true;
            }
            else if (num == 10)
            {
                if (error)
                    clear(0);

                if(now_str.IndexOf(",") == -1)
                    now_str += ",";
            }
            else
            {
                if (!error)
                    if(now_str[0] != '0')
                        if (now_str[0] != '-')
                            now_str = "-" + now_str;
                        else
                            now_str = now_str.TrimStart('-');

            }

            if (!inp_sign)
            {
                a_str = now_str;
                a = Convert.ToDouble(now_str);
            }
            else
            {
                b_str = now_str;
                b = Convert.ToDouble(now_str);
            }    

            print();
        }

        public void input_sign(int type)
        {
            if (error)
                return;
            if (type <= 3)
            {
                if (!inp_b)
                {
                    sign = type;
                    inp_sign = true;

                    if (now_str != "0" && now_str != "")
                    {
                        a = Convert.ToDouble(now_str);
                    }
                    
                    now_str = "";

                    prev = a;
                }
                else
                {
                    input_sign(4);
                    input_sign(type);
                }
            }
            if (type == 4)
            {
                if (inp_b && now_str != "0" && now_str != "")
                {
                    b = Convert.ToDouble(now_str);
                }

                if (!inp_b)
                    b = prev;
                else
                    prev = b;
                switch (sign)
                {
                    case 0:
                        a = a + b;
                        break;

                    case 1:
                        a = a - b;
                        break;

                    case 2:
                        a = a * b;
                        break;

                    case 3:
                        if (b == 0)
                        {
                            error = true;
                            print();
                            return;
                        }

                        a = a / b;
                        break;

                    default:
                        break;
                }

                a_str = a.ToString("0.#######################");

                if (a_str.Length >= 25)
                    error = true;

                inp_sign = false;
                inp_b = false;

                b = 0;

            }
            if (type == 5)
            {
                if (!inp_b && !inp_sign)
                {
                    if (a < 0)
                    {
                        error = true;
                        print();
                        return;
                    }

                    a = Math.Sqrt(a);

                    a_str = a.ToString("0.#######################");
                }
                if (!inp_b && inp_sign)
                {
                    if (a < 0)
                    {
                        error = true;
                        print();
                        return;
                    }

                    b = a;

                    b = Math.Sqrt(b);

                    b_str = b.ToString("0.#######################");

                    inp_b = true;
                }
                if (inp_b && inp_sign)
                {
                    if (b < 0)
                    {
                        error = true;
                        print();
                        return;
                    }

                    b = Math.Sqrt(b);

                    b_str = b.ToString("0.#######################");
                }

                now_str = "";
            }
            if (type == 6)
            {
                if (!inp_b && !inp_sign)
                {
                    if (a == 0)
                    {
                        error = true;
                        print();
                        return;
                    }

                    a = 1 / a;

                    a_str = a.ToString("0.#######################");
                }
                if (!inp_b && inp_sign)
                {
                    if (a == 0)
                    {
                        error = true;
                        print();
                        return;
                    }

                    b = a;

                    b = 1 / b;

                    b_str = b.ToString("0.#######################");

                    inp_b = true;
                }
                if (inp_b && inp_sign)
                {
                    if (b == 0)
                    {
                        error = true;
                        print();
                        return;
                    }

                    b = 1 / b;

                    b_str = b.ToString("0.#######################");
                }

                now_str = "";
            }
            if (type == 7)
            {
                if (!inp_b && !inp_sign)
                {
                    a = 0;

                    a_str = a.ToString("0.#######################");
                }
                if (!inp_b && inp_sign)
                {
                    b = a;

                    b = a * b / 100;

                    b_str = b.ToString("0.#######################");

                    inp_b = true;
                }
                if (inp_b && inp_sign)
                {
                    b = a * b / 100;

                    b_str = b.ToString("0.#######################");
                }

                now_str = "";
            }

            print();
        }

        public void clear(int type)
        {
            if (type == 0)
            {
                a = 0;
                b = 0;

                now_str = "0";
                a_str = "0";
                b_str = "";

                inp_sign = false;
                inp_b = false;

                sign = 0;

                prev = 0;

                error = false;
            }
            if (type == 1)
            {
                if (error)
                    clear(0);

                if (!inp_sign && a != 0 && now_str == "")
                {
                    clear(0);
                    return;
                }

                if (inp_sign && inp_b && b != 00 && now_str == "")
                {
                    b = 0;
                    inp_b = true;

                    now_str = "0";
                    b_str = "";
                }

                if (now_str.Length != 1)
                {
                    now_str = now_str.Remove(now_str.Length - 1);

                    if (now_str.Length == 1 && now_str[0] == '-')
                        now_str = "0";
                }
                else
                    now_str = "0";

                if (!inp_sign)
                {
                    a_str = now_str;

                    if (now_str.Length != 0)
                        a = Convert.ToDouble(now_str);
                }
                else
                {
                    b_str = now_str;
                    if (now_str.Length != 0)
                        b = Convert.ToDouble(now_str);
                }     
            }

            print();
        }

        private void Button_Click(object sender, RoutedEventArgs e) // 0
        {
            input_num(0);
        }

        private void Button_Click_1(object sender, RoutedEventArgs e) // 1
        {
            input_num(1);
        }

        private void Button_Click_2(object sender, RoutedEventArgs e) // 2
        {
            input_num(2);
        }

        private void Button_Click_3(object sender, RoutedEventArgs e) // 3
        {
            input_num(3);
        }

        private void Button_Click_4(object sender, RoutedEventArgs e) // 4
        {
            input_num(4);
        }

        private void Button_Click_5(object sender, RoutedEventArgs e) // 5
        {
            input_num(5);
        }

        private void Button_Click_6(object sender, RoutedEventArgs e) // 6
        {
            input_num(6);
        }

        private void Button_Click_7(object sender, RoutedEventArgs e) // 7
        {
            input_num(7);
        }

        private void Button_Click_8(object sender, RoutedEventArgs e) // 8
        {
            input_num(8);
        }

        private void Button_Click_9(object sender, RoutedEventArgs e) // 9
        {
            input_num(9);
        }

        private void Button_Click_10(object sender, RoutedEventArgs e) // ,
        {
            input_num(10);
        }

        private void Button_Click_13(object sender, RoutedEventArgs e) // +-
        {
            input_num(11);
        }

        private void Button_Click_11(object sender, RoutedEventArgs e) // <-
        {
            clear(1);
        }

        private void Button_Click_12(object sender, RoutedEventArgs e) // C
        {
            clear(0);
        }

        private void Button_Click_14(object sender, RoutedEventArgs e) // +
        {
            input_sign(0);
        }

        private void Button_Click_15(object sender, RoutedEventArgs e) // -
        {
            input_sign(1);
        }

        private void Button_Click_16(object sender, RoutedEventArgs e) // *
        {
            input_sign(2);
        }

        private void Button_Click_17(object sender, RoutedEventArgs e) // /
        {
            input_sign(3);
        }

        private void Button_Click_18(object sender, RoutedEventArgs e) // =
        {
            input_sign(4);
        }

        private void Button_Click_24(object sender, RoutedEventArgs e) // sqrt
        {
            input_sign(5);
        }

        private void Button_Click_25(object sender, RoutedEventArgs e) // 1/x
        {
            input_sign(6);
        }

        private void Button_Click_26(object sender, RoutedEventArgs e) // %
        {
            input_sign(7);
        }

        private void Button_Click_19(object sender, RoutedEventArgs e) // MC
        {
            memory(0);
        }

        private void Button_Click_20(object sender, RoutedEventArgs e) // MR
        {
            memory(1);
        }

        private void Button_Click_21(object sender, RoutedEventArgs e) // MS
        {
            memory(2);
        }

        private void Button_Click_22(object sender, RoutedEventArgs e) // M+
        {
            memory(3);
        }

        private void Button_Click_23(object sender, RoutedEventArgs e) // M-
        {
            memory(4);
        }
    }
}