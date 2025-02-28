import argparse
import sys 

def main(fasta_fp, out_fp, header = None, show_progress_bar = True):
    if show_progress_bar:
        from tqdm import tqdm
        print("")
        waiting_chars = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        j = 0
        with open(fasta_fp, "r") as f:
            line_count = 0
            for line in f:
                line_count += 1
                if line_count%500000 == 0:
                    char = waiting_chars[j]
                    if j == len(waiting_chars)-1:
                        j = 0
                    else:
                        j += 1
                    sys.stdout.write('\r'+ char + ' counting the number of sequences')
            sys.stdout.write('\r✓ counting the number of sequences')
            print("")
        pbar = tqdm(total = line_count // 2, desc = "Sequences")

    fasta_file = open(fasta_fp, "r")
    out_file = open(out_fp, "w")

    # Write header
    if not(header is None):
        for colname in header:
            out_file.write(";{}".format(colname))
        out_file.write("\n")
    id_seq = 0

    for line in fasta_file:
        if line[0] == ">":
            s = str(id_seq) + ";" + str(id_seq) + ";" + line[1:].replace("|",";")
            out_file.write(s)
            id_seq += 1
            if show_progress_bar:
                pbar.update()
    if show_progress_bar:
        pbar.close()        

    fasta_file.close()
    out_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "summarize_fasta", 
                                     description="Read a fasta file and summarizes the headers in a .csv file.")
    parser.add_argument("fasta_fp", type = str, help = "fasta file path")
    parser.add_argument("out_fp", type = str, help = "csv output file")
    parser.add_argument("--header", type = str, default="none", 
                        help = "Column names. If not given, no header is written.", nargs="*")
    parser.add_argument("--progress", action = argparse.BooleanOptionalAction, help = "show progress bar", default=True)
    
    args = parser.parse_args()
    if args.header == "none":
        header = None
    else:
        header = args.header
    
    main(args.fasta_fp, args.out_fp, header = header, show_progress_bar=args.progress)