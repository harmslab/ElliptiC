import pytest
import os

def get_files(base_dir):
    """
    Traverse base_dir and return a dictionary that keys all files and some
    rudimentary *.ext expressions to absolute paths to those files. They keys
    will be things like "some_dir/test0/rocket.txt" mapping to
    "c:/some_dir/life/base_dir/some_dir/test0/rocket.txt". The idea is to have
    easy-to-read cross-platform keys within unit tests.

    Classes of keys:

        + some_dir/test0/rocket.txt maps to a file (str)
        + some_dir/test0/ maps to the test0 directory itself (str)
        + some_dir/test0/*.txt maps to all .txt (list)
        + some_dir/test0/* maps to all files or directories in the directory
          (list)

    Note that base_dir is *not* included in the keys. All are relative to that
    directory by :code:`os.path.basename(__file__)/{base_dir}`.

    Parameters
    ----------
    base_dir : str
        base directory for search. should be relative to test file location.

    Returns
    -------
    output : dict
        dictionary keying string paths to absolute paths
    """

    containing_dir = os.path.dirname(os.path.realpath(__file__))
    starting_dir = os.path.abspath(os.path.join(containing_dir,base_dir))

    base_length = len(starting_dir.split(os.sep))

    # Traverse starting_dir
    output = {}
    for root, dirs, files in os.walk(starting_dir):

        # path relative to base_dir as a list
        this_path = root.split(os.sep)[base_length:]

        # Build paths to specific files
        local_files = []
        for file in files:
            local_files.append(os.path.join(root,file))
            new_key = this_path[:]
            new_key.append(file)
            output["/".join(new_key)] = local_files[-1]

        # Build paths to patterns of file types
        patterns = {}
        ext = list(set([f.split(".")[-1] for f in local_files]))
        for e in ext:
            new_key = this_path[:]
            new_key.append(f"*.{e}")
            output["/".join(new_key)] = glob.glob(os.path.join(root,f"*.{e}"))

        # Build path to all files in this directory
        new_key = this_path[:]
        new_key.append("*")
        output["/".join(new_key)] = glob.glob(os.path.join(root,f"*"))

        # Build paths to directories in this directory
        for this_dir in dirs:
            new_key = this_path[:]
            new_key.append(this_dir)
            # dir without terminating /
            output["/".join(new_key)] = os.path.join(root,this_dir)

            # dir with terminating /
            new_key.append("")
            output["/".join(new_key)] = os.path.join(root,this_dir)

    return output

@pytest.fixture(scope="module")
def example_xyz():
    return get_files(os.path.join("data","example-xyz"))
