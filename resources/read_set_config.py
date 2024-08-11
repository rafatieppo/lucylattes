"""Read and generate setup from config txt file."""


class configSetup:
    """Read config.txt file and return an assignment."""

    def __init__(self):
        """Read config.txt and return."""
        config_file = open('./config_tk.txt', 'r', encoding='UTF-8')
        config_lines = list(config_file.readlines())
        config_file.close()
        self.run_hwebsci = config_lines[6].split(':')[1]
        self.run_indcapes = config_lines[5].split(':')[1]
        self.qf = config_lines[2].split(':')[1]
        self.run_rmcsvfiles = config_lines[4].split(':')[1]

    def run_capes_index(self):
        """Return 1 or 0 from config.txt to run or not capes index."""
        run_indcapes = self.run_indcapes.rstrip('\n')
        run_indcapes = run_indcapes.strip(' ')
        run_indcapes = int(run_indcapes)
        return run_indcapes

    def run_hwebsci_index(self):
        """Return 1 or 0 from config.txt to run or not hwebsci."""
        run_hwebsci = self.run_hwebsci.rstrip('\n')
        run_hwebsci = run_hwebsci.strip(' ')
        run_hwebsci = int(run_hwebsci)
        return run_hwebsci

    def qualis_file(self):
        """Read config file and return which qualis file was assigned."""
        qf = self.qf.rstrip('\n')
        qf = qf.strip(' ')
        return qf

    def run_rm_csvfiles_infolders(self):
        """Return 1 or 0 from config.txt to run or not hwebsci."""
        run_rmcsvfiles = self.run_rmcsvfiles.rstrip('\n')
        run_rmcsvfiles = run_rmcsvfiles.strip(' ')
        run_rmcsvfiles = int(run_rmcsvfiles)
        return run_rmcsvfiles
