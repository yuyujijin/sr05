# license type: free of charge license for academic and research purpose
# see license.txt
# author: Bertrand Ducourthial
# revision: 22/3/22
#
# NB: see in subdirectories for license types and authors of the programs.

# Makefile of the Airplug Software Distribution.
# Layer 1 Makefile (unique main Makefile for the whole distribution)
# NB: this Makefile calls automatically Makefiles in subdirectories.

### GENERAL PARAMETERS #########################################################
# To avoid any problem from the inheritage of SHELL variable from the
# environment
SHELL = /bin/bash

# Language (if the LANGUAGE env variable contains fr, then french, else english)
TEXT = $(shell if [ x`env | grep LANGUAGE | grep fr` = x ] ; then echo "english" ; else echo "french" ; fi )

# Target architecture
# NB: the compiled programs and libraries (as well as object files directories
#     are named according to the ARCH variable used as suffixe in other
#     Makefile. The tgz-bin archive is named according to the ARCH variable.
ARCH ?= $(shell uname -m)

OUTPUT = "airplug-distrib"
VERSION = "22322"


### DIRECTORIES NAMES ##########################################################
# NB: It is assumed that the Airplug convention related to directories
#     organisation is satisfied.

# Exporting the DIR_INSTALL variable for sub-makefiles
export DIR_INSTALL = $(shell pwd)

# List of subdirectories to take into account for building the tgz-dev archive
LISTSUBDIR = $(shell find -maxdepth 1 -mindepth 1 -type d)


### LISTS OF FILES FOR PACKAGING ###############################################
# List of all files for the public archive
# NB: explicit list of subdirectories to avoid including current developments
#     not ready for public distribution.
# NB: this is different for TGZ-DEV which includes all subdirectories.
TGZ_PUB = Makefile license.txt README.pub \
	bin data doc icons input output \
	LIBAPGtk \
	LIBAPGpy \
	APG APG-TEST LIBAPGC \
	WHA WHO WHE \
	EMU RMT LAUNCHTK \
	BAS NET HLG \
	ALT GPS HOP GTW INF \
	BTH SKT \
	COL GRP \
	DFF \
	STO MAP SND SYB \
	VIC	PTH \
	CHT MAP SED TLK IAL

# List of all files for the devel archive, along with subdirectories of
# LISTSUBDIR
TGZ_DEV = Makefile tgz-history license.txt README.pub README.dev \
	$(LISTSUBDIR)

# List of all files and subdirectories for the distribution skeleton archive
TGZ_SKL = Makefile license.txt README.pub \
	bin doc icons input output \
	LIBAPGtk WHAtk WHOtk WHEtk \
	LIBAPGpy WHEpy

# List of all subdirectories for the binary distribution
# Note: this distribution needs at least the skeleton distribution.
TGZ_BIN = Makefile license.txt README.pub \
	LIBAPGC APG APG-TEST


### COMMANDS TO USE ############################################################
# NB: other commands are defined in sub-makefiles

# Make program used for calling sub-makefiles
MAKE = make

# Make options:
#   -s : silent
#   -e : variables which are exported here predominates those initialized in
#        sub-makefiles
# MFLAGS = -e -s
# TODO check -e with APG compilation
MFLAGS = -s


### SPECIFIC RULES #############################################################
# To avoid any problem in case a file has the name of a rule
.PHONY: build clean depend \
	files-tgz-bin files-tgz-dev files-tgz-skl files-tgz-pub \
	help icon incr install list mod-version new-version print-tgz-dev \
	reset secret show-version tgz-bin tgz-pub tgz-dev tgz-skl

# Help rule
# NB: first rule => default rule
help:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(DIR) : aide pour le Makefile de la Suite logicielle Airplug" ; \
		echo "     make build        : compilation" ; \
		echo "     make clean        : suppression des fichiers temporaires" ; \
		echo "     make depend       : calcul des dependances (avant compilation)" ; \
		echo "     make help         : affiche cette aide"; \
		echo "     make icon         : creation de l'icone de l'application" ; \
		echo "     make incr         : similaire a make new-version" ; \
		echo "     make install      : installation du programme (apres compilation)" ; \
		echo "     make list         : liste des fichiers" ; \
		echo "     make mod-version  : modifie la version courante de l'application" ; \
		echo "     make new-version  : cree une nouvelle version de l'application" ; \
		echo "     make reset        : clean + suppression des executables compiles" ; \
		echo "     make secret       : clean + suppression des sources" ; \
		echo "     make show-version : affichage de la version, du type de license et des auteurs" ; \
		echo "     make tgz-bin      : archivage des sources pour distribution binaire" ; \
		echo "     make tgz-pub      : archivage des sources pour distribution publique" ; \
		echo "     make tgz-dev      : archivage des sources pour distribution de developpement" ; \
		echo "     make tgz-skl      : archivage des sources pour embryon de distribution" ; \
	else \
		echo "++++ $(DIR) : help for Makefile of the Airplug Software Distribution" ; \
		echo "     make build        : compilation" ; \
		echo "     make clean        : delete temporary files" ; \
		echo "     make depend       : compute the dependencies (before compilation)" ; \
		echo "     make help         : display this help"; \
		echo "     make icon         : create the application icon" ; \
		echo "     make incr         : same as make new-version" ; \
		echo "     make install      : install the program (after compilation)" ; \
		echo "     make list         : list the files" ; \
		echo "     make mod-version  : modify the current version of the application" ; \
		echo "     make new-version  : create a new version of the application" ; \
		echo "     make reset        : clean + delete the compiled executables" ; \
		echo "     make secret       : clean + delete sources files" ; \
		echo "     make show-version : display the version, the license type and the authors" ; \
		echo "     make tgz-bin      : archive sources for the binary distribution" ; \
		echo "     make tgz-pub      : archive sources for the public distribution" ; \
		echo "     make tgz-dev      : archive sources for the devel distribution" ; \
		echo "     make tgz-skl      : archive sources for the skeleton distribution" ; \
	fi ;


# No application icon nor version management here at layer 1 and this should
# not be propagated to Makefiles of layer 2.
# NB: for the moment, the secret rule is not implemented.
icon incr mod-version new-version secret:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@ => sans effet ici" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule => no effect here" ; \
	fi ;

# These rules are applied on all subdirectories having a layer 2 Makefile.
build depend install list reset:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
	fi ; \
	for R in *; do \
	  	if [ -d $$R ]; then \
			if [ -e $$R/Makefile ]; then \
				$(MAKE) $@ $(MFLAGS) -C $$R ; \
		  else \
				if [ $(TEXT) = "french" ]; then \
					echo "!    $$R : absence de Makefile" ; \
				else \
					echo "!    $$R : no Makefile found" ; \
				fi ; \
			fi ; \
		fi ; \
	done ;


### CLEANING RULES #############################################################
# This rule is applied on the root directory as well as on all
# subdirectories having a layer 2 Makefile.
clean:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
		echo "     suppression des fichiers *~ *.bak *.tgz files-tgz-*" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
		echo "     deleting files *~ *.bak *.tgz files-tgz-*" ; \
	fi ; \
	rm -f *~ *.bak *.tgz files-tgz-* ; \
	for R in *; do \
	  	if [ -d $$R ]; then \
				if [ -e $$R/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$R ; \
		  	else \
					if [ $(TEXT) = "french" ]; then \
						echo "!    $$R : absence de Makefile" ; \
					else \
						echo "!    $$R : no Makefile found" ; \
					fi ; \
				fi ; \
			fi ; \
	done ;


### PACKAGING RULES ############################################################
# This rule is applied on the root directory as well as on all subdirectories
# having a layer 2 Makefile. It produces the file ./files-tgz-bin used by
# the tgz-bin rule. This file contains the list of files to be archived.
files-tgz-bin:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-bin ] ; then \
		rm ./files-tgz-bin ; \
	fi ; \
	for R in $(TGZ_BIN); do \
		if [ -e $$R ]; then \
			echo $$R >> ./files-tgz-bin ; \
			if [ -d $$R ]; then \
				if [ -e $$R/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$R || \
						if [ $(TEXT) = "french" ]; then \
							echo "!    Probleme avec le repertoire $$R" ; \
						else \
							echo "!    Problem with directory $$R" ; \
						fi ; \
					echo "$$R" >> ./files-tgz-bin; \
					for F in `cat $$R/files-tgz-bin` ; do \
						echo "$$R/$$F" >> ./files-tgz-bin; \
					done ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "!    $(OUTPUT) : $$R manquant" ; \
			else \
				echo "!    $(OUTPUT) : $$R not found" ; \
			fi ; \
		fi ; \
	done ;

# This rule is applied on the root directory as well as on all subdirectories
# having a layer 2 Makefile. It produces the file ./files-tgz-dev used by
# the tgz-dev rule. This file contains the list of files to be archived.
files-tgz-dev:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-dev ] ; then \
		rm ./files-tgz-dev ; \
	fi ; \
	for R in $(TGZ_DEV); do \
		if [ -e $$R ]; then \
			echo $$R >> ./files-tgz-dev ; \
			if [ -d $$R ]; then \
				if [ -e $$R/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$R || \
						if [ $(TEXT) = "french" ]; then \
							echo "!    Probleme avec le repertoire $$R" ; \
						else \
							echo "!    Problem with directory $$R" ; \
						fi ; \
					echo "$$R" >> ./files-tgz-dev; \
					for F in `cat $$R/files-tgz-dev` ; do \
						echo "$$R/$$F" >> ./files-tgz-dev; \
					done ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "!    $(OUTPUT) : $$R manquant" ; \
			else \
				echo "!    $(OUTPUT) : $$R not found" ; \
			fi ; \
		fi ; \
	done ;

# This rule is applied on the root directory as well as on all subdirectories
# having a layer 2 Makefile. It produces the file ./files-tgz-pub used by
# the tgz-pub rule. This file contains the list of files to be archived.
files-tgz-pub:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-pub ] ; then \
		rm ./files-tgz-pub ; \
	fi ; \
	for R in $(TGZ_PUB); do \
		if [ -e $$R ]; then \
			echo $$R >> ./files-tgz-pub ; \
			if [ -d $$R ]; then \
				if [ -e $$R/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$R || \
						if [ $(TEXT) = "french" ]; then \
							echo "!    Probleme avec le repertoire $$R" ; \
						else \
							echo "!    Problem with directory $$R" ; \
						fi ; \
					echo "$$R" >> ./files-tgz-pub ; \
					for F in `cat $$R/files-tgz-pub` ; do \
						echo "$$R/$$F" >> ./files-tgz-pub ; \
					done ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "!    $(OUTPUT) : $$R manquant" ; \
			else \
				echo "!    $(OUTPUT) : $$R not found" ; \
			fi ; \
		fi; \
	done ;

# This rule is applied on the root directory as well as on all subdirectories
# having a layer 2 Makefile. It produces the file ./files-tgz-sql used by
# the tgz-skl rule. This file contains the list of files to be archived.
files-tgz-skl:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-skl ] ; then \
		rm ./files-tgz-skl ; \
	fi ; \
	for R in $(TGZ_SKL) ; do \
		if [ -e $$R ]; then \
			echo $$R >> ./files-tgz-skl ; \
			if [ -d $$R ]; then \
				if [ -e $$R/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$R || \
						if [ $(TEXT) = "french" ]; then \
							echo "!    Probleme avec le repertoire $$R" ; \
						else \
							echo "!    Problem with directory $$R" ; \
						fi ; \
					for F in `cat $$R/files-tgz-skl` ; do \
						echo "$$R/$$F" >> ./files-tgz-skl ; \
					done ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "!    $(OUTPUT) : $$R manquant" ; \
			else \
				echo "!    $(OUTPUT) : $$R not found" ; \
			fi ; \
		fi ;\
	done ;

# This rule builds an archive with all files listed into the file
# ./files-tgz-bin produced by the files-tgz-bin rule.
tgz-bin: files-tgz-bin
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
		echo "     fabrication de l'archive $(OUTPUT)-bin-$(ARCH)-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history ; \
		echo "tgz-bin dans `pwd` sur `hostname` le `date +%d"-"%m"-"%Y`" >> tgz-history ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
		echo "     building archive $(OUTPUT)-bin-$(ARCH)-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	  echo "$@ in `pwd` on `hostname` on `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	tar --hard-dereference --no-recursion -czf $(OUTPUT)-bin-$(ARCH)-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-bin` ;

# This rule builds an archive with all files listed into the file
# ./files-tgz-dev produced by the files-tgz-dev rule.
tgz-dev: files-tgz-dev
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
		echo "     fabrication de l'archive $(OUTPUT)-dev-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history ; \
		echo "tgz-dev dans `pwd` sur `hostname` le `date +%d"-"%m"-"%Y`" >> tgz-history ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
		echo "     building archive $(OUTPUT)-dev-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	  echo "$@ in `pwd` on `hostname` on `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	tar --hard-dereference --no-recursion -czf $(OUTPUT)-dev-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-dev` ;

# This rule builds an archive with all files listed into the file
# ./files-tgz-pub produced by the files-tgz-pub rule.
tgz-pub: files-tgz-pub
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
		echo "     fabrication de l'archive $(OUTPUT)-pub-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
		echo "     building archive $(OUTPUT)-pub-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
		echo "$@ in `pwd` on `hostname` on `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	tar --hard-dereference --no-recursion -czf $(OUTPUT)-pub-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-pub` ;

# This rule builds an archive with all files listed into the file
# ./files-tgz-skl produced by the files-tgz-skl rule.
tgz-skl: files-tgz-skl
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
	  echo "     fabrication de l'archive $(OUTPUT)-skl-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
	  echo "     building archive $(OUTPUT)-skl-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
		echo "$@ in `pwd` on `hostname` on `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	tar --hard-dereference --no-recursion -czf $(OUTPUT)-skl-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-skl` ;


### DISTRIB MANAGEMENT RULES ###################################################
# This rule is applied on the root directory as well as on all
# subdirectories having a layer 2 Makefile.
show-version:
	@if [ $(TEXT) = "french" ]; then \
		echo "++++ $(OUTPUT) : regle $@" ; \
		echo "     repertoire d'installation = $(DIR_INSTALL)" ; \
		echo "     version utilisee = $(VERSION)" ; \
		echo "     license   =`cat license | grep "license type:" | cut -d':' -f2`" ; \
		echo "     auteur(s) =`cat license | grep "software author(s):" | cut -d':' -f2`" ; \
	else \
		echo "++++ $(OUTPUT) : $@ rule" ; \
		echo "     install directory = $(DIR_INSTALL)" ; \
		echo "     current version = $(VERSION)" ; \
		echo "     license   =`cat license | grep "license type:" | cut -d':' -f2`" ; \
		echo "     author(s) =`cat license | grep "software author(s):" | cut -d':' -f2`" ; \
	fi ; \
	for R in *; do \
	  if [ -d $$R ]; then \
			if [ -e $$R/Makefile ]; then \
				$(MAKE) $@ $(MFLAGS) -C $$R ; \
		 	else \
				if [ $(TEXT) = "french" ]; then \
					echo "!    $$R : absence de Makefile" ; \
				else \
					echo "!    $$R : no Makefile found" ; \
				fi ; \
			fi ; \
		fi ; \
	done ;
