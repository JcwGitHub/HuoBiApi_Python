#include "FPathHelper.h"


#include <windows.h>
#include <cstring>
#include <string>
#include <tchar.h>
#include <stdlib.h>

#include <iostream>
#include <fstream>

#ifdef QT_DLL
#include "QFileDialog"
#endif // QT_DLL



#define MAXNUMS 256

FPathHelper::FPathHelper()
{
}


FPathHelper::~FPathHelper()
{
}

WCHAR* Convert2WCHAR(const char* InData)
{
	static WCHAR wszClassName[MAXNUMS];
	memset(wszClassName, 0, sizeof(wszClassName));

	MultiByteToWideChar(CP_ACP, 0, InData, (int)strlen(InData) + 1, wszClassName,
		sizeof(wszClassName) / sizeof(wszClassName[0]));
	return wszClassName;
}
char* Convert2Char(WCHAR* InData)
{
	static char charName[MAXNUMS];

	DWORD dwNum = WideCharToMultiByte(CP_OEMCP, NULL, InData, -1, NULL, 0, NULL, FALSE);
	if (dwNum > MAXNUMS)
	{
		return nullptr;
	}

	WideCharToMultiByte(CP_OEMCP, NULL, InData, -1, charName, dwNum, NULL, FALSE);

	return charName;
}

void FPathHelper::ListFiles(std::vector<MD5FileInfo>& OutFiles, const std::string& dir, const std::string& relative)
{
	HANDLE hFind;
	WIN32_FIND_DATA findData;
	LARGE_INTEGER size;

	std::string CurPath = dir + "\\*.*";
	WCHAR* WDir = Convert2WCHAR(CurPath.c_str());
	hFind = FindFirstFile(CurPath.c_str(), &findData);
	if (!hFind)
	{
		return;
	}

	
	while (FindNextFile(hFind, &findData))
	{
		char* CharFile = findData.cFileName;

		//"."或".." 跳过
		if (strcmp(CharFile, ".") == 0 || strcmp(CharFile, "..") == 0)
		{
			continue;
		}

		// 是否是文件夹
		if (findData.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY)
		{
			// 将dirNew设置为搜索到的目录，并进行下一轮搜索 
			std::string LinkStr = dir + "\\" + CharFile;
			std::string Currelative = relative + "\\" + CharFile;

			ListFiles(OutFiles,LinkStr, Currelative);
		}
		else
		{
			size.LowPart = findData.nFileSizeLow;
			size.HighPart = findData.nFileSizeHigh;

			MD5FileInfo FileInfo;
			FileInfo.MD5FileName = std::string(CharFile);
			FileInfo.MD5RelativeFileDir  = relative/* + "\\" + std::string(CharFile)*/;
			FileInfo.MD5AbsoluteFileName = dir + "\\" + std::string(CharFile);
			FileInfo.MD5FileSize = size.QuadPart;
			OutFiles.push_back(FileInfo);

			std::string Text = std::string(CharFile) + "  " + std::to_string(size.QuadPart) + "bytes";
		}
	}

	FindClose(hFind);
}

void FPathHelper::FilterFiles(std::vector<MD5FileInfo>& OutFiles, const std::string& TargetStr)
{
	for (int Index = (int)OutFiles.size() - 1; Index >= 0 ; Index--)
	{
		if (OutFiles[Index].MD5FileName.find(TargetStr.c_str()) != OutFiles[Index].MD5FileName.npos)
		{
			OutFiles.erase(OutFiles.begin() + Index);
		}
	}
}

std::string FPathHelper::GetBinariesPath()
{
	std::string strPaths = "";
#if _UNICODE
	wchar_t Parths[BUFFERLEN];
#else
	char Parths[BUFFERLEN];
#endif
	GetModuleFileName(nullptr, Parths, BUFFERLEN);
	(_tcsrchr(Parths, '\\'))[1] = 0;

#if _UNICODE
	strPaths = Convert2Char(Parths);
#else
	strPaths = Parths;
#endif

	return strPaths;
}
std::string FPathHelper::GetMD5CacheVersionPath()
{
	std::string ProPath = "C:\\BuildVersion.json";
	return ProPath;
}
std::string FPathHelper::GetULCacheManifestForder()
{
	std::string ProPath = FPathHelper::GetBinariesPath();
	ProPath = ProPath.append("CacheVersion\\");
	if (!FPathHelper::DirExists(ProPath))
	{
		CreateDir(ProPath);
	}

	return ProPath;
}

std::string FPathHelper::GetCofigPath()
{
	std::string RootPath = FPathHelper::GetBinariesPath();
	return RootPath.append("/Config");
}

std::string FPathHelper::GetThirdPartyPath()
{
	std::string path = FPathHelper::GetBinariesPath();
	return path.append("/ThirdParty");
}

std::string FPathHelper::GetThirdPartyDllPath()
{
	std::string path = FPathHelper::GetBinariesPath();
	return path.append("/ThirdParty/Libs");
}

bool FPathHelper::DirExists(const std::string& strPath)
{
	DWORD ftyp = GetFileAttributes(strPath.c_str());
	if (ftyp == INVALID_FILE_ATTRIBUTES)
		return false;

	if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
		return true;

	return false;
}

bool FPathHelper::FileExists(const std::string& strPath)
{
	DWORD ftyp = GetFileAttributes(strPath.c_str());
	if (ftyp == INVALID_FILE_ATTRIBUTES)
		return false;

	if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
		return false;

	return true;
}

bool FPathHelper::CreateDir(const std::string& strPath)
{
	bool IsSuccess = true;
	if (FPathHelper::DirExists(strPath))
	{
		return IsSuccess;
	}

	IsSuccess = CreateDirectory(strPath.c_str(), NULL);

	return IsSuccess;
}

std::string FPathHelper::GetTestFile()
{
	std::string path = FPathHelper::GetBinariesPath().append("temporary.txt");
	std::string Content = "Test Connect!";

	if (!FPathHelper::FileExists(path))
	{
		std::ofstream file(path, std::ios::out);
		if (file.is_open())
		{
			file << Content;
		}

		file.close();
	}

	return path;
}

void FPathHelper::OpenURL(const std::string& path)
{
// 	QString TargetFile = StringExten::StdStr2QStr(path);
// 
// 	QProcess process;
// 	TargetFile.replace("/", "\\");
// 	QString cmd = QString("explorer.exe /select,\"%1\"").arg(TargetFile);
// 
// 	process.startDetached(cmd);
}

std::string FPathHelper::ChoseDir()
{
	std::string ChosePath = "";

#ifdef QT_DLL
	ChosePath = FPathHelper::GetBinariesPath() + "/../";
	
	//括号里的参数分别是：指定父类、标题、默认打开后显示的目录、右下角的文件过滤器。
	QString ExportForder = QFileDialog::getExistingDirectory(nullptr, "ProjectRoot", QString(ChosePath.c_str()));
	return ExportForder.toLocal8Bit().toStdString();
#endif // QT_DLL

	return ChosePath;
}

void FPathHelper::DeleteTargetFile(const std::string& path)
{
	if (FileExists(path))
	{
		remove(path.c_str());
	}
}

void FPathHelper::DeleteChar(std::string& path, const char* Targt)
{
	do
	{
		int pos = path.find(Targt);
		if (pos > -1)
		{
			path.erase(pos, 1);
		}
		else
		{
			break;
		}
	} while (1);
}

void FPathHelper::ChangeFF(std::string& path, const char* source /*= "\\\\"*/, const char* target /*= "/"*/)
{
	do
	{
		int Index = path.find(source);
		if (Index > -1)
		{
			path.replace(Index, 2, target);
		}
		else
		{
			break;
		}
	} while (1);
}

void FPathHelper::DealPath(std::string& path)
{
	do
	{
		int Index = path.find("//");
		if (Index > -1)
		{
			path.replace(Index, 2, "/");
		}
		else
		{
			break;
		}
	} while (1);

	do
	{
		int Index = path.find("\\/");
		if (Index > -1)
		{
			path.replace(Index, 2, "/");
		}
		else
		{
			break;
		}
	} while (1);
}
