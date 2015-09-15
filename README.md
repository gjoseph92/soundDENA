## soundDB

Structure, or, how this thing works
===================================

soundDB's primary job is to describe the structure of soundscape data on disk, and make bulk querying and processing of it easy. To be as easily reconfigurable as possible, the specifics of this "structure of soundscape data on disk" are broken out into three levels, each of which uses the previous. (Note that every type of file has its own function for each of these levels.)

From lowest-level to highest-level:

    + A **Reader** parses a specific type of data file off the disk. Given the path to a file, it knows how to read it into a pandas DataFrame.
    + An **Accessor** knows where to find a specific type of file within a site's data directory, and the Reader needed to load it. Given the path to a data directory (or site ID), it locates and loads the file into a DataFrame using the assocaited Reader.
    + A **Mapper** applies the Accessor for a specific type of file across multiple sites, handling errors and missing data.

For example, NVSPL has a Reader that can parse the file's CSV format (`soundDB.readers.nvspl`), an accessor that knows NVSPL is found in `site_folder\01 DATA\NVSPL` (`soundDB.accessors.nvspl`), and a mapper which can grab the NVSPL for all the sites you want (`soundDB.nvspl`).

Accessors and Readers will rarely be used directly. You'll almost always just give the top-level Mapper method an iterable of sites to access (i.e. `soundDB.nvspl(["DENAWOCR2015", "DENAMURI2015"])`).

### Reconfiguration

Thanks to these three levels, changes should be easy to adapt to. If a file's structure changes, modify its Reader. If its location changes, modify the Accessor. Mappers are actually auto-generated for each Accessor, but if the general mapping logic needs to change (say, how to handle missing data), a change to the one higher-order `_mapper` function will apply to all mappers.

**Example: handling a new type of file**

Say we've added a CSV file computing the average drag coefficient per day to every site. For example, it's found at `2013 DENAFANG Fang Mountain\02 ANALYSIS\Computational Outputs\DENAFANG_drag.csv`.

We need a Reader to parse this type of file:

```python
# In readers.py
def drag(path):
    return pd.to_csv(path)
```

Also, we need an Accessor to locate the file within a site's folder, and say which Reader can open it. The higher-order `_accessor` function generates an Accessor function for you; just pass it the Reader to use, and where to find the file. (In the filepath, `{unit}`, `{site}`, and `{year}` will be filled in with the appropriate values for each site.)

```python
# In accessors.py
drag = _accessor(readers.drag, paths.computed / "{unit}{site}_drag.csv")
```

That's it! The Mapper will be created automatically: every function in `accessors.py` gets wrapped with a Mapper. Now you can use `soundDB.drag(["DENAFANG2013", "DENATHRI2015", ...])`, as well as `soundDB.accessors.drag` and `soundDB.readers.drag`.
