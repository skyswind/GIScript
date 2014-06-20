#!/bin/bash
#  ============================================================================>
# 
#   this file it predection supermap ugo environment   
#   Company: SuperMap Software Co., Ltd @2005-2011
#
#  ============================================================================>
#
#check lib
CurrentLib=""
#ugc dir
CurrentLibPath=""
#split LD_LIBRARY_PATH
filesArray=""
#LIB VERSION
Version=""
Debug=""
ORACLE_HOME_LIB=""
Check_dir=$PWD

Record_All_File=""
Record_File=""

#record the error

HelpSegment()
{
	echo "resolve this error"
	#if [ -n $1 ]
	#then
	#	echo "1. chcon -t texrel_shlib_t $1"
	#else
		echo "1. chcon -t texrel_shlib_t *.so"
	#fi
	
	echo "2. Disabling SELinux altogether by setting the line"
   	echo "SELinux=disabled"
   	echo "in your /etc/sysconfig/selinux file"
   	echo "then reboot you system"
}

EXIT_()
{
	if [ -z $Record_File ]
	then
		date
	else
		date >> $Record_File  
	fi
	exit $1
}


Fatal()
{
	if [ -z $Record_File ]
	then
		echo -n "Fatal: "  
		while [ -n "$1" ]
		do
			echo -n " $1"  
			shift 1
		done
		echo ""
	else
		echo -n "Fatal: ">> $Record_File  
		while [ -n "$1" ]
		do
			echo -n " $1" >>$Record_File 
			shift 1
		done
		echo "">>$Record_File
	fi
	EXIT_ 1
}

Error()
{
	if [ -z $Record_File ]
	then
		echo -n "Error: "  
		while [ -n "$1" ]
		do
			echo -n " $1"  
			shift 1
		done
		echo ""
	else
		echo -n "Error: ">> $Record_File  
		while [ -n "$1" ]
		do
			echo -n " $1" >>$Record_File 
			shift 1
		done
		echo "">>$Record_File
	fi
}

#record the message
Message()
{
	
	echo -n "Message:"
	while [ -n "$1" ]
	do
		echo -n " $1"
		shift 1
	done
	echo " "
}

Warning()
{
	if [ -z $Record_File ]
	then
		echo -n "Waring: "  
		while [ -n "$1" ]
		do
			echo -n " $1"  
			shift 1
		done
		echo ""
	else
		echo -n "Waring: ">> $Record_File  
		while [ -n "$1" ]
		do
			echo -n " $1" >>$Record_File 
			shift 1
		done
		echo "">>$Record_File
	fi
}

#checklib is 32bit or 64bit
#check linuxlibs is 32or64bit 64 return 1 32bit return 0 others return -1
ChecksLib()
{
	#echo "checklib  $CurrentLib" 
	count=`readelf -h $CurrentLib|grep -c 'ELF32'`  
	if [ -f $CurrentLib ]
	then
		if [ $count -eq 0 ] 
		then
			return  1
		else
			return  0
		fi
	else
		return -1
	fi  
}

RemoveFile()
{
	if [ -f $1 ]
	then
		rm -rf $1
	fi
}

#ishow all input lib
checkis32or64bit()
{
	ChecksLib
	result=$?
	if [ $result -eq 0 ]
        then
        	return 0;
	elif [ $result -eq 1 ]
        then
        	Fatal $CurrentLib" is 64bit Please set 32bit to LD_LIBRARY_PATH"

        elif [ $result -eq -1 ]
        then
        	Fatal $CurrentLib is dir 
        fi
}

# split LD_LIBRARY_PATH for analyst
#if support AIX here will split LIBPATH

splitld_library_path()
{
	OLD_IFS="$IFS"
        IFS=":"
	filesArray=($LD_LIBRARY_PATH)
	IFS="$OLD_IFS"
}

# Check UGO DIR is pro in order for UGO run
CheckLibDir()
{
	echo "Check UGODIR..."
	i=0  #record filesArray Pos
	length=${#filesArray[@]} #record filesArray Length
	#find the ugcroot
	for item in ${filesArray[@]}
	do
		files=$item"/libSuBase"$Debug".so"
		if [ -f $files ]
		then
			CurrentLibPath=$item
			Message "UGC dir:"$CurrentLibPath
			break	
		fi
		i=$(expr $i + 1)
	done
	
	if [ $i -eq $length ]
	then
		Fatal "f0001 not find ugo dir; please add ugo dir in LD_LIBRARY_PATH"
	elif [ $i -lt $length -a $i -eq 0 ]
	then
		Message "m0001 Check UGO dir OK"
	elif [ $i -lt $length -a $i -gt 0 ]
	then
		Warning "w0001 you'd better put ugo dir to the first of LD_LIBRARY_PATH "
	fi	
}


#check SuperMapRoot,LC_ALL,LANG,SUPERMAP_CHARSET.if we will support other language
#here wil modified to all language check
CheckOtherPath()
{
	echo "Check SuperMapRoot...."
	SuperMapRoot=$SUPERMAP_ROOT
	if [ -z $SuperMapRoot ]
	then
		SuperMapRoot=$UGCROOT
	fi		
	
	if [ -z $SuperMapRoot ]
	then
		Error "e0001 Please  export SUPERMAP_ROOT environment"
	elif [ -d $SuperMapRoot -a -r $SuperMapRoot ]
	then
		if [ ! -f $SuperMapRoot"/fonts/simsun.ttc" -o ! -r $SuperMapRoot"/fonts/simsun.ttc" ]
		then
			Error "e0002 Please add simsun.ttc in $SUPERMAP_ROOT/fonts"
		else
			Message "m0002 SupermapRoot is OK"
		fi
	else
		echo "Check SuperMapRoot is normal"
	fi
	
	
	echo "Check language environment..."
	if [ ! -z $LC_ALL ]
	then
		if [ ! $LC_ALL = "zh_CN.gbk" ]
		then 
			Error "e0004 Please export LC_ALL=zh_CN.gbk for GBK"
		fi
	
	else
		Error "e0004 Please export LC_ALL"
	fi

	if [ ! -z $SUPERMAP_CHARSET ]
	then
		if [ ! $SUPERMAP_CHARSET = "zh_CN.gbk" ]
		then 
			Warning "w0010 Please export SUPERMAP_CHARSET=zh_CN.gbk for GBK"
		fi
	
	else
		if [ ! -z $LANG ]
		then
			if [ ! $LANG = "zh_CN.gbk" ]
			then 
				Warning "w0011 Please export LANG=zh_CN.gbk for GBK"
			fi
		else
			Warning "w0011 Please export LANG or SUPERMAP_CHARSET =  zh_CN.gbk for zh Envrionment"
 		fi
	fi
        Message "m0003 check language complete "
		
}

#check some error in library if found some new error Please add here

CheckLibisOK()
{
	cd $CurrentLibPath
	file=$1
	
	if [ ! -f $file ]
	then
		Error "e0010" "not a relgar file $file"
		return 1
	fi
	
	count=`more .tmptest | grep -c 'Floating point exception'`
	if [ $count -gt 0 ]
	then
		Error "e0011 $file not support in this platform find floating point exception please using static lib"
		return 1	
	fi
	
	count=`more .tmptest|grep -c 'not a dynamic executable'`
	if [ $count -gt 0 ]
	then
		Error "e0012 $file not a dynamic executable"
		return 1	
	fi
	
	output=`more .tmptest|grep 'cannot restore segment prot after reloc'`
	for item in ${output[@]} 
	do
		length=`expr length $item`
		if [ -n $item ]
		then
			Error "e0013" $item 
			HelpSegment 
		fi

		return 1	
	done
	
	more .tmptest | grep 'not found' | sed -e 's/^[[:blank:]]*//' -e 's/ =>.*//' > .tmp
	sort .tmp  > .tmp2
	files=`uniq .tmp2`
	for item in ${files[@]}
	do
		Error "e0014" "Please put "$item" in LD_LIBRARY_PATH depended by "$1
		RemoveFile .tmp
		RemoveFile .tmp2
		return 1
	done	
	RemoveFile .tmp
	RemoveFile .tmp2

	count=`more .tmptest | grep -c 'undefined symbol'`
	if [ $count -gt 0 ]
	then
		Error "e0015" "some symbol not define Please use -write argument "
		if [ ! -z $Record_File ]
		then	
			output=`more .tmptest | grep 'undefined symbol'`
			echo "####################$file have some undefined symbol#######################">>$Record_File
			echo $output>>$Record_File
		fi	
		return 1
	fi
	
	count=`more .tmptest | grep -c 'error:'`
	if [ $count -gt 0 ]
	then		
		output=`more .tmptest |grep 'error:'`
		Error "e0016" $output 
		return 1	
	fi	
	
	count=`more .tmptest | grep -c 'warning:'`
	if [ $count -gt 0 ]
	then		
		Warning "w0030" "$file"
		output=`more .tmptest |grep "warning:"`
		Warning $output 
	fi
	return 0
	
}


CheckDependsLibDepends()
{
	ldd $1 2>/dev/null| sed -e 's/^[[:blank:]]*//' -e 's/ .*=>//' > .tmps
	files=`uniq .tmps`
	Commond_2=`echo $1|grep -c "libSuEngineOracle$Debug.sdx"`
	if [ $Commond_2 -eq 1 ]
	then
		Commond_1=`more .tmptest | grep -c "libclntsh"`
		if [ $Commond_1 -eq 1 ]
		then
			ORACLE_HOME_LIB=$CurrentLib
		fi
	fi
	rm -rf .tmps 2>/dev/null

}


#move LibDir depended lib to libdir
CheckDependsLib()
{
	
	echo "Check Wrapj..."
	item="libWrapj.so"
	ldd -r $item >.tmptest 2>&1 
	CheckLibisOK $item
	#RemoveFile .tmptest
	if [ ! $? -eq 0 ]
	then
		Fatal " f0010 Wrapj check doesn't pass"
	fi
	echo "Check Depends Lib..."
	cd $CurrentLibPath
	#files=`find . -name "libSu*.sdx"`
	files=`find . -name "libSu*.*"`
	for item in ${files[@]}
	do
		length1=`expr index $item "./"`
		length2=`expr length $item`
		itemall=`expr substr "$item" 3 $length2`
		lastfix=`echo $itemall |cut -d "." -f2`
		if [ -f $itemall ]
		then
			if [ ! $lastfix = "so" ]
			then
				echo "Check Lib $itemall..."
				ldd -r $item >.tmptest 2>&1 
				CheckDependsLibDepends $itemall
				CheckLibisOK $itemall
				RemoveFile .tmptest
			fi
		fi
		#echo $files		
	done
}



CheckDependsLibVersion()
{
	echo "Check Depends Lib Version..."
}


CheckOracleEnvironment()
{
	echo "check oracle environment..."
	if [ -z "$NLS_LANG" ]
	then
		Warning "w0020" "NLS_LANG must equal with server"
	else
		Message "m0020" "check NLS_LANG equal with server"
	fi
	
	#if [ -z "$ORACLE_HOME_LIB" ]
	#then
	#	Error "e0020" "Oracle_HOME check dosen't pass" 
	#	return 1
	#fi
	
	
	if [ ! -f $ORACLE_HOME"/network/admin/tnsnames.ora" ]
	then
		Error "e0021" "tnsname.ora dosen't found please check ORACLE_HOME"
		return 1
	fi
	
	#length=`expr index "$ORACLE_HOME_LIB" "$ORACLE_HOME"`
	#if [ $length -eq 1 ]
	#then
	#	Message "m0021" "OracleHome OK"
	#else
	#	Error "e0022" "Please put libclntns to LD_LIBRARY_PATH"
	#fi
}

RecordAllInfor()
{
	if [ ! -z $Record_All_File ]
	then
		echo "env info #################" >>$Record_All_File
		env >> $Record_All_File
		cd $CurrentLibPath
		echo "getconf LONG_BIT#################" >>$Record_All_File
		getconf LONG_BIT >> $Record_All_File	
		echo "/proc/version#################" >>$Record_All_File
		cat /proc/version >> $Record_All_File	
		echo "pciinfo#################" >>$Record_All_File
		lspci >> $Record_All_File	
		echo "glxinfo#################" >>$Record_All_File
		glxinfo >> $Record_All_File	
		echo "meminfo#################" >>$Record_All_File
		cat /proc/meminfo >> $Record_All_File	
		echo "cpuinfo#################" >>$Record_All_File
		cat /proc/cpuinfo >> $Record_All_File	
		echo "issue info#################" >>$Record_All_File
		cat /etc/issue >> $Record_All_File	
		echo "uname info#################" >>$Record_All_File
		uname -a >> $Record_All_File	
		echo "dmidecode info#################" >>$Record_All_File
		dmidecode >> $Record_All_File	
#		eecho "#################" >>$Record_All_File
#		files=`find . -name "lib*.*"`
#		for item in ${files[@]}
#                do		
#			echo $item>>$Record_all_File
#			ldd -r $item 2>&1 |xargs -0 echo  >>$Record_All_File
#			echo "################################">>$Record_All_File
#		done
	fi
}

help()
{
	echo "OPTIONS:"
	echo "-h              help "
	echo "-write=filename"
	echo "                write error,warning,error informaton to filename"
	echo "                if filename is null, will write to errorreport.txt" 
	echo "-write-all=filename" 
	echo "                if have this argument, this shell will collect computer information to filename for support"
	echo "                if filename is null, will write to inforeport.txt"
	echo "EXAMPLE:        chmod +x ./predetection.sh; ./predetection.sh"
        EXIT_ 0;
}


#input parameter check
while [ -n "$1" ]
do
	case $1 in
	-h)     
		help
                ;;
	-write-all=*) 
                Record_All_File=`echo $1 |sed -e "s/^-write-all=\(.*\)/\1/g"`
		if [ -z $Record_All_File ]
		then
			Record_All_File="inforeport.txt" 
		fi
		echo "write some computer information to File $Record_All_File"
		shift 1
	 	continue	
		;;
	-write-all) 
		Record_All_File="inforeport.txt" 
		echo "write some computer information to File $Record_All_File"
		shift 1
		continue
		;;
	-write=*)	
                Record_File=`echo $1 |sed -e "s/^-write=\(.*\)/\1/g"`
		if [ -z $Record_File ]
		then
			Record_File="errorreport.txt" 
		fi
		
		echo "write error warning to File $Record_File"
		shift 1
		continue	
               ;;
	-write)
		Record_File="uerrorreport.txt" 
		echo "write error warning to File $Record_File"
		shift 1
		continue
		;;
        *)
		echo "unknow argument $1"
		help
		;;
	esac
done

	splitld_library_path		
	CheckLibDir
	RecordAllInfor
	CheckOtherPath
	CheckDependsLib
	CheckOracleEnvironment
        EXIT_ 0	
