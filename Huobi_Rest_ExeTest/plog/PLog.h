#pragma once
#include "plog/Log.h"
#include "plog/Appenders/ColorConsoleAppender.h"

#include "Windows.h"
#include <stdarg.h>
#include <cstring>
#include <tchar.h>
#include <libloaderapi.h>


enum class FLog
{
	none = 0,
	fatal = 1,
	error = 2,
	warning = 3,
	info = 4,
	debug = 5,
	verbose = 6
};

#define P_LOGTXT(p)						PLOG_(1, (plog::Severity)p)
#define P_LOG(p)						PLOG_(0, (plog::Severity)p)
#define P_LOGALL(p,p1)					PLOG_(0, (plog::Severity)p) << ##p1;\
										PLOG_(1, (plog::Severity)p) << ##p1;
#define P_STR(p,...)					CustomPlog::CombStr(p,__VA_ARGS__);


namespace CustomPlog
{
#define MAXNUMS 256
#define BUFFERLEN 64

	static WCHAR* Convert2WCHAR(const char* InData);
	WCHAR* Convert2WCHAR(const char* InData)
	{
		static WCHAR wszClassName[MAXNUMS];
		memset(wszClassName, 0, sizeof(wszClassName));

		MultiByteToWideChar(CP_ACP, 0, InData, strlen(InData) + 1, wszClassName,
			sizeof(wszClassName) / sizeof(wszClassName[0]));
		return wszClassName;
	}

	static char* Convert2Char(WCHAR* InData);
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

	static bool DirExists(const std::string& strPath);
	bool DirExists(const std::string& strPath)
	{
		DWORD ftyp = GetFileAttributes(strPath.c_str());
		if (ftyp == INVALID_FILE_ATTRIBUTES)
		{
			return false;
		}
		if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
		{
			return true;
		}
		return false;
	}

	static bool CreateDir(const std::string& strPath);
	bool CreateDir(const std::string& strPath)
	{
		bool IsSuccess = true;
		if (CustomPlog::DirExists(strPath))
		{
			return IsSuccess;
		}
		IsSuccess = CreateDirectory(strPath.c_str(), NULL);
		return IsSuccess;
	}

	static int ListDirFiles(const std::string& dir);
	int ListDirFiles(const std::string& dir) 
	{
		int FileNums = 0;
		HANDLE hFind;
		WIN32_FIND_DATA findData;
		//LARGE_INTEGER size;

		std::string CurPath = dir + "\\*.*";
		hFind = FindFirstFile(CurPath.c_str(), &findData);
		if (!hFind)
		{
			return FileNums;
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
				continue;
			}
			
			FileNums++;
		}

		FindClose(hFind);

		return FileNums;
	}

	static std::string GetBinariesPath();
	std::string GetBinariesPath()
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
		strPaths = CustomPlog::Convert2Char(Parths);
#else
		strPaths = Parths;
#endif

		return strPaths;
	}

	static char* CombStr(const char* fmt, ...);
	char* CombStr(const char* fmt, ...)
	{
		static char GTemp[512];
		va_list args;
		va_start(args, fmt);
		vsprintf_s(GTemp, fmt, args);
		va_end(args);

		return GTemp;
	}

	struct FLogInit
	{
		FLogInit()
		{
			static bool IsInit = false;
			if (!IsInit)
			{
				//log初始化
				static plog::ColorConsoleAppender<plog::TxtFormatter> consoleAppender;
				plog::init<0>(plog::info, &consoleAppender);
				PLOGI_(0) << "plog Init Console";

				std::string logPath = CustomPlog::GetBinariesPath() + "log";
				if (CustomPlog::DirExists(logPath) || CustomPlog::CreateDir(logPath))
				{
					logPath = logPath + CombStr("\\log%d.txt", ListDirFiles(logPath));
				}
				else
				{
					logPath = "c:\\log.txt";
				}

				plog::init<1>(plog::info, logPath.c_str());
				PLOGI_(0) << "plog Init file : " << logPath << "\n";
				IsInit = true;
			}
		}
	};
	static CustomPlog::FLogInit GLogIit;
}

