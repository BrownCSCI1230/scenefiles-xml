import os
import time
import shutil
import subprocess

testTemp = "temp"
testConfigs = "temp/test_configs"
testOutputs = "temp/test_outputs"

basePath = os.getcwd()

testTempPath = os.path.join(basePath, testTemp)
testConfigsPath = os.path.join(basePath, testConfigs)
testOutputsPath = os.path.join(basePath, testOutputs)

testsToRun = { 
    "test_unit",
    "test_intersect",
    "test_efficiency",
    "test_light",
    # "test_legacy",
    # "test_feature",
    # "test_fun",
    # "test_refract",
    # "test_dof",
    # "test_take_forever",
    # "test_mesh",
}

testConfigParams = {
    "test_unit": {
        "shadows": "false",
        "reflect": "false",
        "refract": "false",
        "texture": "false",
        "parallel": "false",
        "super-sample": "false",
        "acceleration": "false",
        "depthoffield": "false",
        "texture-filter": "false",
    },
    "test_intersect": {
        "shadows": "false",
        "reflect": "false",
        "refract": "false",
        "texture": "false",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "false",
    },
    "test_light": {
        "shadows": "true",
        "reflect": "true",
        "refract": "false",
        "texture": "true",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "false",
    },
    "test_feature": {
        "shadows": "true",
        "reflect": "true",
        "refract": "false",
        "texture": "true",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "false",
    },
    "test_fun": {
        "shadows": "true",
        "reflect": "true",
        "refract": "false",
        "texture": "true",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "true",
    },
    "test_efficiency": {
        "shadows": "true",
        "reflect": "true",
        "refract": "true",
        "texture": "true",
        "parallel": "false",
        "super-sample": "false",
        "acceleration": "false",
        "depthoffield": "false",
        "texture-filter": "false",
    }, 
    "test_refract": {
        "shadows": "true",
        "reflect": "true",
        "refract": "true",
        "texture": "true",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "true",
    }, 
    "test_dof": {
        "shadows": "true",
        "reflect": "true",
        "refract": "true",
        "texture": "true",
        "parallel": "true",
        "super-sample": "false",
        "acceleration": "true",
        "depthoffield": "true",
        "texture-filter": "true",
    },
    "test_take_forever": {
        "shadows": "true",
        "reflect": "true",
        "refract": "true",
        "texture": "true",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "true",
    },
    "test_mesh": {
        "shadows": "true",
        "reflect": "true",
        "refract": "true",
        "texture": "true",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "true",
    },
    "test_legacy": {
        "shadows": "false",
        "reflect": "false",
        "refract": "false",
        "texture": "false",
        "parallel": "true",
        "super-sample": "true",
        "acceleration": "true",
        "depthoffield": "false",
        "texture-filter": "true",
    },
}

def generateTestFiles(basePath, testName, filename):
    if not testName in testConfigParams.keys():
        raise "cannot find test: " + testName
    
    filenameNoExt = filename.split(".")[0]
    configFileName = testName + "_" + filenameNoExt
    configFilePath = os.path.join(testConfigsPath, configFileName) + ".ini"
    outputFilePath = os.path.join(testOutputsPath, configFileName) + ".png"
    
    if os.path.exists(configFilePath):
        os.remove(configFilePath)

    params = testConfigParams[testName]

    with open(configFilePath, "w") as f:
        f.write("[IO]\n")
        f.write("\tscene = " + os.path.join(basePath, testName, filename) + "\n")
        f.write("\toutput = " + outputFilePath + "\n")
        f.write("\n")

        f.write("[Canvas]\n")
        f.write("\twidth = 1024\n")
        f.write("\theight = 768\n")
        f.write("\n")
        
        f.write("[Feature]\n")
        for key, value in params.items():
            f.write("\t{0} = {1}\n".format(key, value))

    return

if __name__ == "__main__":
    # clean existing folders
    if os.path.exists(testTempPath):
        shutil.rmtree(testTempPath)

    os.mkdir(testTempPath)
    os.mkdir(testConfigsPath)
    os.mkdir(testOutputsPath)

    # get all test folders
    allTestFolders = [file for file in os.listdir(".") if file.startswith("test_") and os.path.isdir(file)]

    # generate test config files
    for testFolder in allTestFolders:
        if not testFolder in testsToRun:
            continue

        fullPath = os.path.join(basePath, testFolder)
        allSceneFiles = [file for file in os.listdir(fullPath) if file.endswith(".xml")]
        for filename in allSceneFiles:
            generateTestFiles(basePath, testFolder, filename)

    # check if the ray tracer executable exist
    raytracer = os.path.join(basePath, "projects_ray")

    if not os.path.exists(raytracer):
        raise "Ray Tracer executable not exists"

    # discover all tests to run
    allTestConfigsPath = [os.path.join(testConfigsPath, file) for file in os.listdir(testConfigsPath)]
    allTestConfigsPath.sort()

    start = time.time()

    # run all tests while suppressing stdout output
    for config in allTestConfigsPath:
        print(raytracer + " " + config)
        subprocess.run([raytracer, config], stdout=subprocess.DEVNULL)

    end = time.time()

    print("Take {:.6f} seconds to render all scenes".format(end - start))
