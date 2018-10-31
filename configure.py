#      Example configuration script for adding/working with data in fyda      #
# --------------------------------------------------------------------------- #
#                                                                             #
# Uncomment everything below and run this script in command line to configure #
# fyda. You can then open up python and poke around at the configuration      #
# values. The iris, X, and y data sets are available as examples within this  #
# repository if you want to get a feel for working with fyda.                 #
# --------------------------------------------------------------------------- #

# def main():
#     """Main execution."""
#     # Leave this statement alone
#     fyda.configurate.ALLOW_OVERWRITE = True
# 
#     # Configure your data root. By default this is <path/to/this/file>/data
#     fyda.set_data_root(
#         os.path.join(
#             os.path.dirname(os.path.abspath(__file__)),
#             'data'))
# 
#     # Add any other directories you may need access to.
#     fyda.add_directory(
#         raw=os.path.join(
#             fyda.dir_path('input_folder'),
#             'raw'),
#         output=os.path.join(
#             fyda.dir_path('input_folder'),
#             'output'),
#         processed=os.path.join(
#             fyda.dir_path('input_folder'),
#             'processed'))
# 
#     # Add the data shortcuts
#     fyda.add_data(
#         iris=os.path.join('raw', 'iris.csv'),
#         X=os.path.join('processed', 'X.npy'),
#         y=os.path.join('processed', 'y.npy'),
#         add_options=True)
# 
# 
# if __name__ == '__main__':
#     main()
