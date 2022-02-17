# 修改pom
import os
import argparse
from utils import *
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE

ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')
path_base = None
modify_list = None
is_debug = None

def parse_args():
    global path_base, modify_list, is_debug
    parser = argparse.ArgumentParser()
    parser.add_argument('-ml', '--modifies', help='list project names that need to modify. "," as delimiter')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    path_base = get_path_base()
    modify_list = get_list(args.modifies, path_base, 'modify')
    is_debug = args.debug

def modify_pom(path):
    # print('modify file {} ...'.format(path))
    tree = ET.parse(path)
    root = tree.getroot()

    # build parent map
    tree.parent_map = dict((c, p) for p in tree.getiterator() for c in p)
    # remove spotbugs maven plugin
    allPlugins = list(root.iter('{http://maven.apache.org/POM/4.0.0}plugin'))
    for plugin in allPlugins:
        for element in plugin:
            if (element.tag == '{http://maven.apache.org/POM/4.0.0}artifactId'):
                if (element.text == 'spotbugs-maven-plugin'):
                    tree.parent_map[plugin].remove(plugin)
                break

    # add spotbugs maven plugin
    root = tree.getroot()
    buildElement = root.find('{http://maven.apache.org/POM/4.0.0}build')
    if buildElement == None:
        buildElement = ET.SubElement(root, '{http://maven.apache.org/POM/4.0.0}build')

    pluginsElement = buildElement.find('{http://maven.apache.org/POM/4.0.0}plugins')
    if pluginsElement == None:
        pluginsElement = ET.SubElement(buildElement, '{http://maven.apache.org/POM/4.0.0}plugins')

    plugin = ET.SubElement(pluginsElement, '{http://maven.apache.org/POM/4.0.0}plugin')
    groupId = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}groupId')
    groupId.text = 'com.github.spotbugs'
    artifactId = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}artifactId')
    artifactId.text = 'spotbugs-maven-plugin'
    version = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}version')
    version.text = '4.2.3-SNAPSHOT'
    configuration = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}configuration')
    visitors = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}visitors')
    visitors.text = 'FindFieldSelfAssignment,FindLocalSelfAssignment2,BadUseOfReturnValue,FindFloatEquality,VolatileUsage,DontUseEnum,InheritanceUnsafeGetResource,IncompatMask,SynchronizeOnClassLiteralNotGetClass,SerializableIdiom,FindSelfComparison,FindSelfComparison2,DontCatchIllegalMonitorStateException,FindRoughConstants,Naming,MethodReturnCheck,InefficientIndexOf,FindDeadLocalStores,FindUselessControlFlow,URLProblems,DumbMethodInvocations,OverridingEqualsNotSymmetrical,QuestionableBooleanAssignment,UnnecessaryMath,FormatStringChecker,FindFinalizeInvocations,BadSyntaxForRegularExpression,NumberConstructor,FindRefComparison,StaticCalendarDetector,InfiniteRecursiveLoop,FindPuzzlers,WaitInLoop,FindBadCast2,FindUnrelatedTypesInGenericContainer,DumbMethods,TestASM'
    include_filter_file = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}includeFilterFile')
    include_filter_file.text = '/home/codegex/git/codegex/spotbugs-includeFilter.xml'
    effort = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}effort')
    effort.text = 'Default'
    threshold = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}threshold')
    threshold.text = 'Low'
    if is_debug:
        debug = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}debug')
        debug.text = 'true'
    # xmlOutput = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}xmlOutput')
    # xmlOutput.text = 'true'
    # xmlOutputDirectory = ET.SubElement(configuration, '{http://maven.apache.org/POM/4.0.0}xmlOutputDirectory')
    # xmlOutputDirectory.text = '{}/{}'.format(report_mvn, filename)
    dependencies = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}dependencies')
    dependency = ET.SubElement(dependencies, '{http://maven.apache.org/POM/4.0.0}dependency')
    groupId = ET.SubElement(dependency, '{http://maven.apache.org/POM/4.0.0}groupId')
    groupId.text = 'com.github.spotbugs'
    artifactId = ET.SubElement(dependency, '{http://maven.apache.org/POM/4.0.0}artifactId')
    artifactId.text = 'spotbugs'
    version = ET.SubElement(dependency, '{http://maven.apache.org/POM/4.0.0}version')
    version.text = '4.1.4'
    # reporting
    # reportingElement = root.find('{http://maven.apache.org/POM/4.0.0}reporting')
    # if reportingElement == None:
    #     reportingElement = ET.SubElement(root, '{http://maven.apache.org/POM/4.0.0}reporting')
    # pluginsElement = reportingElement.find('{http://maven.apache.org/POM/4.0.0}plugins')
    # if pluginsElement == None:
    #     pluginsElement = ET.SubElement(reportingElement, '{http://maven.apache.org/POM/4.0.0}plugins')
    # plugin = ET.SubElement(pluginsElement, '{http://maven.apache.org/POM/4.0.0}plugin')
    # groupId = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}groupId')
    # groupId.text = 'com.github.spotbugs'
    # artifactId = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}artifactId')
    # artifactId.text = 'spotbugs-maven-plugin'
    # version = ET.SubElement(plugin, '{http://maven.apache.org/POM/4.0.0}version')
    tree.write(open(path, 'w'), encoding='unicode')


def is_success(filename):
    if not os.path.exists(filename):
        return False
    openfile = open(filename, 'r')
    content = openfile.read()
    if 'spotbugs-includeFilter.xml' in content:
        return True
    else:
        return False


if __name__ == '__main__':
    parse_args()
    print('[Modify] start modifying {} projects. is_debug: {}'.format(str(len(modify_list)), str(is_debug)))
    for filename in modify_list:
        cwd = os.path.join(path_base, filename)
        pipe = Popen(['find', cwd, '-name', 'pom.xml', '-not', '-path', '*/target/*'], stdout=PIPE, cwd=cwd);
        allPomXml = pipe.communicate()[0].decode("utf-8").splitlines()
        for pomXml in allPomXml:
            modify_pom(pomXml)
        print("[Project] {} done".format(filename))
    print("[Modify] Done.")
