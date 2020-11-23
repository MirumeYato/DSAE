DSAE - Data Science Analysis Error for multiple charged particle modeling programm

   ------------------------------------------------------------
For 29.10.2020 It is just a mini-progect, which create a .db of 
modeling  error  results  for  multiply-charged  particles with 
different  charge and  mass and  with special parameter -  type 
name of variation in modeling. Program asking you the way to 
directory with results of modeling, pars names of directories 
and in each directory serch log.out file and pars it for result 
meaning of difference (error)
   ------------------------------------------------------------


Please read below before start work with
==Commands=====================================================
[config]=======================================================
Command config is used to set main settings - 1) name path to 	
file system with analysis data (inside must be situated 	
directories with names like: 

	"submitDir_(data-time)_M(*)_Z(*)_(variation name)"),
2) name path to work directory (where program should save .db),
3) name of .db file (where program write data from file sys).

	Options:

	-d/--default - make command faster. It will ask only
		"1)" item. Another items will be completed
		automatically with default meanings.

	[!] In case error - file settings.ini will be deleted 
	(or saved unchanged if it exists)
===============================================================

[mkdir]========================================================
Command mkdir is used only for copy date from your file system 
to a single .db file. After that you already can to sort or 
collect data in some special way by using  [***] command. 
Without adding options would be runed DEFAULT mode.

	Options:

	-d/--default - uses path parameters from config file
		(settings.ini), pars file system and write 
		data from each correct log.out file to .db .
		Subsequent command calls will rewrite .db
		file (if it exist).
	-u/--upgrade - uses path parameters from config file
		(settings.ini), pars the same like DEFAULT 
		mode, but only rewrite "old" data in .db to
		new data created month and earlier.
	-c/--create  - uses path parameters from config file
		(settings.ini) + you can choose rewrite 
		existing .db (if it is) or name new. Then it 
		pars the same like DEFAULT mode, but choose
		only new data created month and earlier.

	[!] In case error - file .db will be deleted
	(or saved unchanged if it exists)
===============================================================

[***]==========================================================
...

	Options:

	-d/--default - ...
	...
===============================================================



==non-defined-charapter========================================
1) When you answer to confirmation (question y\n) some times 
you will see "Y\n" or "y\N". That [caps] means the "default 
answer" - if you skipped (answered to) question by printing 
Enter).

2) Any time you can leave programm with ^C (^Z). But it will 
delete current file with progress. We recommend you copy your
config file for saving paths if it too long.
===============================================================