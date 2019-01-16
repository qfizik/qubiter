from EchoingSEO_reader import *


class EngLineList:
    """
    Eng=English File

    In programs like PyQuil (by Rigetti) and Cirq (by Google), circuits (aka
    programs) are stored in memory essentially as Python lists of gates.
    Lists of this type can be sliced, combined, etc. They are very
    convenient, more flexible than English files, when one wants to load the
    whole circuit into memory, so as to be able to randomly access any gate
    of it at will. This is convenient, for instance, when doing circuit
    optimizations (i.e., replacing the circuit by an equivalent but
    hopefully shorter one, what IBM qiskit calls "transpiling").

    In this class, we support Qubiter's version of PyQuil's and Cirq's gate
    lists. In Qubiter, we use simply a Python list of the lines, stored as
    strings, of the circuit's English file.

    Attributes
    ----------
    line_list : list[str]
    num_bits : int

    """
    def __init__(self, line_list, num_bits):
        """
        Constructor

        Returns
        -------

        """
        self.line_list = line_list
        self.num_bits = num_bits

    @staticmethod
    def eng_file_to_line_list(file_prefix, num_bits):
        """
        This static method reads an English file with file prefix
        `file_prefix` and it returns a list of its line strings.

        Parameters
        ----------
        file_prefix : str
        num_bits : int

        Returns
        -------
        list[str]

        """
        path = file_prefix + '_' + str(num_bits) + '_eng.txt'
        with open(path, 'r') as f:
            line_list = [line.rstrip('\n') for line in f]
        return line_list

    @staticmethod
    def line_list_to_eng_and_pic_files(line_list, file_prefix, num_bits):
        """
        This method does the reverse of eng_file_to_line_list(). It writes
        both an English file and a Picture file with file prefix=file_prefix.

        Parameters
        ----------
        line_list : list[str]
        file_prefix : str
        num_bits : int

        Returns
        -------
        None

        """
        end_str = '_' + str(num_bits) + '_eng.txt'
        with open(file_prefix + end_str, 'w') as f:
            for line in line_list:
                f.write(line + '\n')

        # this writes a Picture file from the English file just created
        EchoingSEO_reader.pic_file_from_eng_file(file_prefix, num_bits)

    def print(self):
        """
        prints self.line_list, one item per line

        Returns
        -------
        None

        """
        print('\n'.join(self.line_list))

    def write_eng_and_pic_files(self, file_prefix):
        """
        This method does the same as line_list_to_eng_and_pic_files(),
        except it is called by an object of this class instead of being a
        static method.

        Parameters
        ----------
        file_prefix : str

        Returns
        -------
        None

        """
        EngLineList.line_list_to_eng_and_pic_files(
            self.line_list, file_prefix, self.num_bits)

    def get_var_nums_list(self):
        """
        This method returns a list of all the distinct variable numbers
        encountered.

        Returns
        -------
        list[int]

        """
        var_nums_list = []
        for line in self.line_list:
            split_line = line.split()
            for token in split_line:
                if SEO_writer.is_legal_var_name(token):
                    if token[0] == '#':
                        var_num = int(token[1:])
                    else:  # starts with '-#':
                        var_num = int(token[2:])
                    if var_num not in var_nums_list:
                        var_nums_list.append(var_num)
        return var_nums_list

    def __add__(self, other):
        """
        define + of two EngFileList objects

        Parameters
        ----------
        other : EngLineList

        Returns
        -------
        EngLineList

        """
        assert self.num_bits == other.num_bits
        return EngLineList(self.line_list + other.line_list, self.num_bits)

    def __getitem__(self, item):
        """
        define self[item]

        Parameters
        ----------
        item : slice

        Returns
        -------
        EngLineList

        """
        return EngLineList(self.line_list[item], self.num_bits)

if __name__ == "__main__":
    def main():
        num_bits = 4
        file_prefix = 'io_folder/eng_line_list_test'
        emb = CktEmbedder(num_bits, num_bits)
        wr = SEO_writer(file_prefix, emb)
        wr.write_Rx(2, rads=np.pi/7)
        wr.write_Rx(1, rads='#2')
        wr.write_Rn(3, rads_list=['#1', '-#1', '#3'])
        wr.write_cnot(2, 3)
        wr.close_files()

        li = EngLineList.eng_file_to_line_list(file_prefix, num_bits)
        ell = EngLineList(li, num_bits)

        print("\nell print")
        ell.print()
        print('ell var_nums_list=\n', ell.get_var_nums_list())

        ell.write_eng_and_pic_files(file_prefix + '_ditto')

        print("\nell[1:] print")
        ell[1:].print()

        ell_sum = ell + ell

        print("\nell_sum print")
        ell_sum.print()
        print('ell_sum var_nums_list=\n', ell_sum.get_var_nums_list())
    main()