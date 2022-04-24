# license type: free of charge license for academic and research purpose
# see license.txt
# author: Bertrand Ducourthial
# revision: 24/09/2021

# Layer 2 makefile of the Airplug Software Distribution for directory without subdirectories
# See the file Makefile-var for directory-dependent configuration.

VERSION="24septembre2021"

### GENERAL PARAMETERS #########################################################
# To avoid any problem from the inheritage of SHELL variable from the
# environment
SHELL = /bin/bash

# Language (if the LANGUAGE env variable contains fr, then french, else english)
TEXT = $(shell if [ x`env | grep LANGUAGE | grep fr` = x ] ; then echo "english" ; else echo "french" ; fi )

# For underline in list rule
BU=`tput smul`
EU=`tput rmul`


### DIRECTORIES NAMES ##########################################################
# Exporting the DIR variable for sub-makefiles
export DIR=$(shell pwd | rev | cut -d'/' -f 1 | rev)

# Install directory of the whole distribution
DIR_INSTALL = ..


### COMMANDS TO USE ############################################################

MAKE = make

# make options:
# -s : silent
# -e : variables which are exported here predominates those initialized in sub-makefiles
MFLAGS = -e -s

###  APPLICATION DEPENDENT VARIABLES ###########################################
# NB: any specificity is defined in Makefile-var to keep a generic Makefile.
# NB: any previously defined variable could be overwritten in Makefile-var
#     preserving the genericity of the Makefile.
include Makefile-var

# To avoid any problem in case a file has the name of a rule
.PHONY: build clean depend icon files-tgz-dev files-tgz-skl files-tgz-pub \
	help icon incr install list mod-version new-version print-tgz-dev reset \
	show-version tgz-pub tgz-dev tgz-skl

# First rule = default rule (help)
help:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : aide pour le Makefile de la Suite logicielle Airplug" ; \
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
		echo "     make show-version : affichage de la version, du type de license et des auteurs" ; \
		echo "     make tgz-pub      : archivage des sources pour distribution publique" ; \
		echo "     make tgz-dev      : archivage des sources pour distribution de developpement" ; \
		echo "     make tgz-skl      : archivage des sources pour embryon de distribution" ; \
	else \
		echo " +++ $(DIR) : help for Makefile of the Airplug Software Distribution" ; \
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
		echo "     make show-version : display the version, the license type and the authors" ; \
		echo "     make tgz-pub      : archive sources for the public distribution" ; \
		echo "     make tgz-dev      : archive sources for the devel distribution" ; \
		echo "     make tgz-skl      : archive sources for the skeleton distribution" ; \
	fi;

build depend icon incr mod-version new-version print-tgz-dev reset show-version:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@ => sans effet ici" ; \
	else \
		echo " +++ $(DIR) : $@ rule => no effect here" ; \
	fi;

clean:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
		echo "     suppression des *~ *bak *tgz files-tgz-* et des liens cassés" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
		echo "     deleting *~ *bak *tgz files-tgz-* and broken links" ; \
	fi ; \
	rm -f *~ *bak *tgz files-tgz-* `find -L . ! -readable` ; \
	for F in $(SOURCES) ; do \
		if [ -d $$F ]; then \
			if [ -e $$F/Makefile ]; then \
				$(MAKE) $@ $(MFLAGS) -C $$F ; \
			else \
				if [ $(TEXT) = "french" ]; then \
					echo " !   $(DIR) : absence de Makefile dans $(DIR)/$$F" ; \
				else \
					echo " !   $(DIR) : no Makefile in $(DIR)/$$F" ; \
				fi ; \
			fi ; \
		fi ; \
	done ;


files-tgz-dev:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-dev ] ; then \
		rm ./files-tgz-dev ; \
	fi ; \
	for F in $(TGZ_DEV) ; do \
		if [ -e $$F ]; then \
			echo $$F >> ./files-tgz-dev ; \
			if [ -d $$F ]; then \
				if [ -e $$F/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$F ; \
					for G in `cat $$F/files-tgz-dev` ; do \
						echo "$$F/$$G" >> ./files-tgz-dev ; \
					done ; \
				else \
					if [ $(TEXT) = "french" ]; then \
						echo " !   $(DIR) : absence de Makefile dans $(DIR)/$$F" ; \
					else \
						echo " !   $(DIR) : no Makefile in $(DIR)/$$F" ; \
					fi ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "! $(DIR) : $$F manquant" ; \
			else \
				echo "! $(DIR) : $$F not found" ; \
			fi ; \
		fi ; \
	done ; \

files-tgz-pub:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-pub ] ; then \
		rm ./files-tgz-pub ; \
	fi ; \
	for F in $(TGZ_PUB) ; do \
		if [ -e $$F ]; then \
			echo $$F >> ./files-tgz-pub ; \
			if [ -d $$F ]; then \
				if [ -e $$F/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$F ; \
					for G in `cat $$F/files-tgz-pub` ; do \
						echo "$$F/$$G" >> ./files-tgz-pub ; \
					done ; \
				else \
					if [ $(TEXT) = "french" ]; then \
						echo " !   $(DIR) : absence de Makefile dans $(DIR)/$$F" ; \
					else \
						echo " !   $(DIR) : no Makefile in $(DIR)/$$F" ; \
					fi ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "! $(DIR) : $$F manquant" ; \
			else \
				echo "! $(DIR) : $$F not found" ; \
			fi ; \
		fi ; \
	done ; \

files-tgz-skl:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
	fi ; \
	if [ -e ./files-tgz-skl ] ; then \
		rm ./files-tgz-skl ; \
	fi ; \
	for F in $(TGZ_SKL) ; do \
		if [ -e $$F ]; then \
			echo $$F >> ./files-tgz-skl ; \
			if [ -d $$F ]; then \
				if [ -e $$F/Makefile ]; then \
					$(MAKE) $@ $(MFLAGS) -C $$F ; \
					for G in `cat $$F/files-tgz-skl` ; do \
						echo "$$F/$$G" >> ./files-tgz-skl ; \
					done ; \
				else \
					if [ $(TEXT) = "french" ]; then \
						echo " !   $(DIR) : absence de Makefile dans $(DIR)/$$F" ; \
					else \
						echo " !   $(DIR) : no Makefile in $(DIR)/$$F" ; \
					fi ; \
				fi ; \
			fi ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "! $(DIR) : $$F manquant" ; \
			else \
				echo "! $(DIR) : $$F not found" ; \
			fi ; \
		fi ; \
	done ; \

instal install:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
		echo "     repertoire de la distribution : $(DIR_INSTALL)" ; \
		echo "     repertoire des sources : $(DIR)" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
		echo "     install directory : $(DIR_INSTALL)" ; \
		echo "     sources directory : $(DIR)" ; \
	fi ;
# Appicon for Window Maker
# NB: only for the icons directory which owns the icon
	@if [ -e ./apg-icon-default.ppm ]; then \
		if [ -e ~/GNUstep/Library/Icons ]; then \
			if [ $(TEXT) = "french" ]; then \
				echo "     lien vers apg-icon-default.ppm dans ~/GNUstep/Library/Icons (Window Maker)" ; \
			else \
				echo "     link towards apg-icon-default.ppm in ~/GNUstep/Library/Icons (Window Maker)" ; \
			fi ; \
			ln -sf --target-directory ~/GNUstep/Library/Icons `pwd`/apg-icon-default.ppm ; \
		else \
			if [ $(TEXT) = "french" ]; then \
				echo "     Window Maker non present, pas d'installation de l'icone par defaut" ; \
			else \
				echo "     Window Maker not found, no installation of the default icon" ; \
			fi ; \
		fi ; \
	fi ;

list:
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
	fi ; \
	echo "     Sources : $(SOURCES)" ; \
	if [ -d $(DIR_INSTALL)/dev ]; then \
		echo "     ${BU}Makefiles${EU} :" ; \
		for M in $(DIR_INSTALL)/dev/Makefiles/Makefile* ; do \
			if [ "`stat --printf %i $$M`" = "`stat --printf %i Makefile`" ]; then \
				echo "     Makefile     --> $$M" ; \
			fi ; \
			if [ -e Makefile-var ] && [ "`stat --printf %i $$M`" = "`stat --printf %i Makefile-var`" ]; then \
				echo "     Makefile-var --> $$M" ; \
			fi ; \
			if [ -e Makefile-bin ] && [ "`stat --printf %i $$M`" = "`stat --printf %i Makefile-bin`" ]; then \
				echo "     Makefile-bin --> $$M" ; \
			fi ; \
		done ; \
	fi ; \
	for F in $(SOURCES) ; do \
		if ! [ -e $$F ]; then \
			if [ $(TEXT) = "french" ]; then \
				echo "! $(DIR) : $$F manquant" ; \
			else \
				echo "! $(DIR) : $$F not found" ; \
			fi ; \
		fi; \
	done ;

tgz-pub: files-tgz-pub
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
	  echo "     fabrication de l'archive airplug-$(DIR)-$(VERSION)-pub-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
	  echo "     building archive airplug-$(DIR)-$(VERSION)-pub-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	if [ $(TEXT) = "french" ]; then \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history ; \
	else	\
		echo "$@ in `pwd` on `hostname`, `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	tar --no-recursion -czf airplug-$(DIR)-$(VERSION)-pub-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-pub` ;


tgz-dev: files-tgz-dev
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
		echo "     fabrication de l'archive airplug-$(DIR)-$(VERSION)-dev-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
		echo "     building archive airplug-$(DIR)-$(VERSION)-dev-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	if [ $(TEXT) = "french" ]; then \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history ; \
	else \
		echo "$@ in `pwd` on `hostname`, `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	tar --no-recursion -czf airplug-$(DIR)-$(VERSION)-dev-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-dev` ;


tgz-skl: files-tgz-skl
	@if [ $(TEXT) = "french" ]; then \
		echo " +++ $(DIR) : regle $@" ; \
	 	echo "     fabrication de l'archive airplug-$(DIR)-$(VERSION)-skl-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	else \
		echo " +++ $(DIR) : $@ rule" ; \
	 	echo "     building archive airplug-$(DIR)-$(VERSION)-skl-`hostname`-`date +%Y"-"%m"-"%d`.tgz" ; \
	fi ; \
	if  ! [ -e tgz-history ] ; then \
		touch tgz-history ; \
	fi ; \
	if [ $(TEXT) = "french" ]; then \
		echo "$@ dans `pwd` sur `hostname` le `date +%A" "%d" "%B" "%Y" a "%k"h"%M":"%S`" >> tgz-history ; \
	else \
		echo "$@ in `pwd` on `hostname`, `date +%A" "%d" "%B" "%Y" at "%k"h"%M":"%S`" >> tgz-history ; \
	fi ; \
	tar --no-recursion -czf airplug-$(DIR)-$(VERSION)-skl-`hostname`-`date +%Y"-"%m"-"%d`.tgz `cat files-tgz-skl` ;


