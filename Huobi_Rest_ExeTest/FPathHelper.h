#pragma once
#include <string>
#include <vector>
#include <map>
#include <basetsd.h>

#define FFLINK					"\\"
#define MANIFEST				"Manifest.json"
#define UP_VERSION_NAME			"UpVersion"
#define DOWN_VERSION_NAME		"DownVersion"
#define BUFFERLEN				64

/**
 * MD5
 */
struct MD5FileInfo
{
	//MD5
	std::string MD5AbsoluteFileName;
	std::string MD5RelativeFileDir;
	std::string MD5FileName;
	std::string MD5Value;
	INT64		MD5FileSize;

	//Launch
	std::string LaunchCache;
	std::string LaunchProject;

	//根目录的Exe为工程名
	std::string ProName;
	std::string ProNameMD5;

	MD5FileInfo()
	{
		MD5FileSize = 0;
	}
};
typedef std::vector<MD5FileInfo> FileArray;
typedef std::map<std::string, MD5FileInfo> FileMap;


/**
 * 版本信息
 */
class MD5Manifest
{
public:
	int UpVersion = 0;
	int DownVersion = 0;

	FileMap AllFiles;

	void Reset()
	{
		UpVersion = 0;
		DownVersion = 0;
		AllFiles.clear();
	}
};


/**
 * 路径
 */
class FPathHelper
{
public:
	FPathHelper();
	~FPathHelper();

	static void ListFiles(std::vector<MD5FileInfo>& OutFiles, const std::string& dir,const std::string& relative = "");
	static void FilterFiles(std::vector<MD5FileInfo>& OutFiles,const std::string& TargetStr);

public:
	/************************MD5*******************************************/
	static std::string GetMD5CacheVersionPath();
	/************************************************************************/
	
	/************************Launch客户端************************************/
	static std::string GetULCacheManifestForder();
	/************************************************************************/

	//exe路径
	static std::string GetBinariesPath();

	//Config 路径
	static std::string GetCofigPath();

	//第三方路径
	static std::string GetThirdPartyPath();

	//第三方DLL
	static std::string  GetThirdPartyDllPath();

	//文件夹是否存在
	static bool DirExists(const std::string& strPath);


	//文件是否存在
	static bool FileExists(const std::string& strPath);

	static bool CreateDir(const std::string& strPath);

	/************************************************************************/
	/* 文件/文件夹                                                     */
	/************************************************************************/
	//测试文件
	static std::string GetTestFile();
	//打开文件夹
	static void OpenURL(const std::string& path);
	//选择文件夹
	static std::string ChoseDir();
	//删除文件
	static void DeleteTargetFile(const std::string& path);
	//删除字节
	static void DeleteChar(std::string& path, const char* Targt);
	static void ChangeFF(std::string& path,const char* source = "\\\\", const char* target = "/");
	static void DealPath(std::string& path);
};

