import argparse
import os
import time
import shutil
import subprocess
from multiprocessing import Process

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
    "test_light",
    "test_efficiency",
    "test_feature",        # For Project 4: Illuminate
    # "test_fun",          # For Project 4: Illuminate (optional)
    # "test_legacy",       # Not really relevant
    # "test_refract",      # For extra credit (refraction)
    # "test_dof",          # For extra credit (depth of field)
    # "test_take_forever", # For extra credit (acceleration datastructure / parallelism)
    # "test_mesh",         # For extra credit (triangle mesh intersection)
}

testConfigParams = {
    "test_unit": {
        "shadows":        "false",
        "reflect":        "false",
        "refract":        "false",
        "texture":        "false",
        "parallel":       "false",
        "super-sample":   "false",
        "acceleration":   "false",
        "depthoffield":   "false",
        "texture-filter": "false",
    },
    "test_intersect": {
        "shadows":        "false",
        "reflect":        "false",
        "refract":        "false",
        "texture":        "false",
        "parallel":       "false",
        "super-sample":   "false",
        "acceleration":   "false",
        "depthoffield":   "false",
        "texture-filter": "false",
    },
    "test_light": {
        "shadows":        "true", # false for Intersect
        "reflect":        "true", # false for Intersect
        "refract":        "false",
        "texture":        "true", # false for Intersect
        "parallel":       "false",
        "super-sample":   "false",
        "acceleration":   "false",
        "depthoffield":   "false",
        "texture-filter": "false",
    },
    "test_efficiency": {
        "shadows":        "true", # false for Intersect
        "reflect":        "true", # false for Intersect
        "refract":        "false",
        "texture":        "true", # false for Intersect
        "parallel":       "false",
        "super-sample":   "false",
        "acceleration":   "false",
        "depthoffield":   "false",
        "texture-filter": "false",
    }, 
    "test_feature": {
        "shadows":        "true",
        "reflect":        "true",
        "refract":        "false",
        "texture":        "true",
        "parallel":       "false",
        "super-sample":   "false",
        "acceleration":   "false",
        "depthoffield":   "false",
        "texture-filter": "false",
    },
    "test_fun": {
        "shadows":        "true",
        "reflect":        "true",
        "refract":        "false",
        "texture":        "true",
        "parallel":       "true",
        "super-sample":   "true",
        "acceleration":   "true",
        "depthoffield":   "false",
        "texture-filter": "true",
    },
    "test_refract": {
        "shadows":        "true",
        "reflect":        "true",
        "refract":        "true",
        "texture":        "true",
        "parallel":       "true",
        "super-sample":   "true",
        "acceleration":   "true",
        "depthoffield":   "false",
        "texture-filter": "true",
    }, 
    "test_dof": {
        "shadows":        "true",
        "reflect":        "true",
        "refract":        "true",
        "texture":        "true",
        "parallel":       "true",
        "super-sample":   "false",
        "acceleration":   "true",
        "depthoffield":   "true",
        "texture-filter": "true",
    },
    "test_take_forever": {
        "shadows":        "true",
        "reflect":        "true",
        "refract":        "true",
        "texture":        "true",
        "parallel":       "true",
        "super-sample":   "true",
        "acceleration":   "true",
        "depthoffield":   "false",
        "texture-filter": "true",
    },
    "test_mesh": {
        "shadows":        "true",
        "reflect":        "true",
        "refract":        "true",
        "texture":        "true",
        "parallel":       "true",
        "super-sample":   "true",
        "acceleration":   "true",
        "depthoffield":   "false",
        "texture-filter": "true",
    },
    "test_legacy": {
        "shadows":        "false",
        "reflect":        "false",
        "refract":        "false",
        "texture":        "false",
        "parallel":       "true",
        "super-sample":   "true",
        "acceleration":   "true",
        "depthoffield":   "false",
        "texture-filter": "true",
    },
}

def generateTestFiles(basePath, testName, filename):
    if not testName in testConfigParams.keys():
        raise "cannot find test: " + testName
    
    filenameNoExt = filename.split(".")[0]
    configFileName = testName + "_" + filenameNoExt
    configFilePath = os.path.join(testConfigsPath, configFileName) + ".ini"
    configFilePath = configFilePath.replace("\\", "/")
    outputFilePath = os.path.join(testOutputsPath, configFileName) + ".png"
    outputFilePath = outputFilePath.replace("\\", "/")
    
    if os.path.exists(configFilePath):
        os.remove(configFilePath)

    params = testConfigParams[testName]

    with open(configFilePath, "w") as f:
        f.write("[IO]\n")
        f.write("\tscene = " + os.path.join(basePath, testName, filename).replace("\\", "/") + "\n")
        f.write("\toutput = " + outputFilePath + "\n")
        f.write("\n")

        f.write("[Canvas]\n")
        f.write("\twidth = 512\n")
        f.write("\theight = 384\n")
        f.write("\n")
        
        f.write("[Feature]\n")
        for key, value in params.items():
            f.write("\t{0} = {1}\n".format(key, value))

    return


def renderTests(raytracer, allTestConfigsPath):
    start = time.time()

    # run all tests while suppressing stdout output
    for config in allTestConfigsPath:
        print(raytracer + " " + config)
        subprocess.run([raytracer, config])

    end = time.time()
    print("Take {:.6f} seconds to render all scenes".format(end - start))
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--timeout', default=-1,
                        help='The timeout for rendering in seconds. A negative value means no timeout')

    args = parser.parse_args()
    timeout = int(args.timeout)

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
        fullPath = fullPath.replace("\\", "/")
        allSceneFiles = [file for file in os.listdir(fullPath) if file.endswith(".xml")]
        for filename in allSceneFiles:
            generateTestFiles(basePath, testFolder, filename)

    # check if the ray tracer executable exist
    raytracer = os.path.join(basePath, "projects_ray.exe")
    raytracer = raytracer.replace("\\", "/")

    if not os.path.exists(raytracer):
        raise "Ray Tracer executable not exists"

    # discover all tests to run
    allTestConfigsPath = [os.path.join(testConfigsPath, file).replace("\\", "/") for file in os.listdir(testConfigsPath)]
    allTestConfigsPath.sort()

    for x in allTestConfigsPath: print(x)

    p = Process(target=renderTests, args=[raytracer, allTestConfigsPath])
    p.start()

    if timeout <= 0:
        p.join()
    else:
        p.join(timeout)
        
    if p.exitcode is None:
        p.terminate()
        print("did not finished rendering within the given time:", timeout, "seconds")
    elif p.exitcode != 0:
        print("process teminated with a non-zero exitcode")
    else:
        print("success")

        # add suffix to output image
        for f in os.listdir(testOutputsPath):
            name, ext = f.split(".")
            name += "_gen"
            newF = ".".join([name, ext])
            newF = newF.replace("\\", "/")

            os.rename(os.path.join(
              testOutputsPath, f).replace("\\", "/"),
              os.path.join(testOutputsPath, newF).replace("\\", "/")
            )

        # copy images from bench folder
        assignmentName = "grading_illuminate"
        benchImagesFolder = os.path.join(basePath, "bench", assignmentName)

        allBenchImages = [f for f in os.listdir(benchImagesFolder) if f.startswith("test_")]
        allBenchImages.sort()
        imagesToCopy = []

        for image in allBenchImages:
            for testName in testsToRun:
                if image.startswith(testName):
                    imagesToCopy.append(image)
                    break
            
        for image in imagesToCopy:
            src = os.path.join(benchImagesFolder, image)
            
            name, ext = image.split(".")
            name += "_ref"
            dst = os.path.join(testOutputsPath, ".".join([name, ext]))
            dst = dst.replace("\\", "/")
            shutil.copy(src, dst)